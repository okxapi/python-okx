import threading
import time

from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor
from twisted.internet.error import ReactorAlreadyRunning

from . import WsUtils
from .WsClientFactory import *


class WsConnectManager(threading.Thread):

    def __init__(self, url, isPrivate):
        threading.Thread.__init__(self)
        self.factories = {}
        self.isPrivate = isPrivate
        self._connected_event = threading.Event()
        self.url = url
        self.conns = {}
        self.callback = None
        self.logger = logging.getLogger(__name__)

    def subscribeSocket(self, args: list, callback):
        channelArgs = {}
        channelParamMap = {}
        WsUtils.checkSocketParams(args, channelArgs, channelParamMap)
        if len(channelArgs) < 1:
            return False
        for channel in channelArgs:
            subSet = channelParamMap.get(channel, set())
            if self.isPrivate:
                privateKey = self.getPrivateKey(channel)
                if privateKey not in self.factories:
                    reactor.callFromThread(self.loginSocket, channel)
                    time.sleep(2)
                    newFactory = self.initSubscribeFactory(args=channelArgs[channel], subSet=subSet, callback=callback)
                    reactor.callFromThread(self.resetConnection, newFactory, channel)
                    continue
            factory = self.initSubscribeFactory(args=channelArgs[channel], subSet=subSet, callback=callback)
            self.factories[channel] = factory
            reactor.callFromThread(self.addConnection, channel)

    def unsubscribeSocket(self, args: list, callback):
        channelArgs = {}
        channelParamMap = {}
        WsUtils.checkSocketParams(args, channelArgs, channelParamMap)
        if len(channelArgs) < 1:
            return False
        for channel in channelArgs:
            if self.isPrivate:
                privateKey = self.getPrivateKey(channel)
            else:
                privateKey = channel
            if privateKey not in self.factories:
                continue
            factory = self.factories[privateKey]
            ifFiledParams = factory.subscribeSet - channelParamMap[channel]
            if len(ifFiledParams) < 1:
                self.disconnect(channel)
            else:
                payload = json.dumps({"op": "unsubscribe", "args": channelArgs[channel]}, ensure_ascii=False).encode(
                    "utf8")
                factory = WsClientFactory(self.url, payload=payload)
                factory.client = self
                factory.protocol = WsClientProtocol
                factory.callback = callback
                factory.subscribeSet = ifFiledParams
                reactor.callFromThread(self.resetConnection, factory, channel)

    def addConnection(self, channel):
        self.conns[channel] = connectWS(self.factories[channel])

    def disconnect(self, channel):
        if channel not in self.conns:
            self.logger.error("WsConnectManager disconnect error,channel is not able".format(channel))
            return
        self.conns[channel].factory = WebSocketClientFactory(self.url)
        self.conns[channel].disconnect()
        del self.conns[channel]
        privateKey = channel
        if self.isPrivate:
            privateKey = self.getPrivateKey(channel)
        del self.factories[privateKey]

    def initSubscribeFactory(self, args, subSet: set, callback):
        payload = json.dumps({"op": "subscribe", "args": args}, ensure_ascii=False).encode(
            "utf8")
        factory = WsClientFactory(self.url, payload=payload)
        factory.payload = payload
        factory.protocol = WsClientProtocol
        factory.callback = callback
        factory.subscribeSet = factory.subscribeSet | subSet
        return factory

    def loginSocket(self, channel: str):
        payload = WsUtils.initLoginParams(useServerTime=self.useServerTime, apiKey=self.apiKey,
                                          passphrase=self.passphrase, secretKey=self.secretKey)
        factory = WsClientFactory(self.url, payload=payload)
        factory.protocol = WsClientProtocol
        factory.callback = loginSocketCallBack
        privateKey = self.getPrivateKey(channel)
        self.factories[privateKey] = factory
        self.conns[channel] = connectWS(factory)

    def resetConnection(self, newFactory, channel):
        if self.isPrivate:
            privateKey = self.getPrivateKey(channel)
            preFactory = self.factories[privateKey]
        else:
            preFactory = self.factories[channel]
        instance = preFactory.instance
        if instance is None:
            raise ValueError("instance must not none")
        instance.factory = newFactory
        instance.payload = newFactory.payload
        instance.onConnect(None)

    def getPrivateKey(self, channel) -> str:
        return str(self.apiKey) + "@" + channel

    def run(self):
        try:
            reactor.run(installSignalHandlers=False)
        except ReactorAlreadyRunning as e:
            self.logger.error("WsConnectManager reactor.run error;e:{}".format(e))

    def close(self):
        keys = set(self.conns.keys())
        for key in keys:
            self.closeConnection(key)
        self.conns = {}


def loginSocketCallBack(message):
    print("loginSocket callback:", message)
