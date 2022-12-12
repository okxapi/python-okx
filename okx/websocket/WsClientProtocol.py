import json
import logging

from autobahn.twisted.websocket import WebSocketClientProtocol


class WsClientProtocol(WebSocketClientProtocol):
    def __init__(self, factory, payload=None):
        super().__init__()
        self.autoPingInterval = 5
        self.factory = factory
        self.payload = payload
        self.logger = logging.getLogger(__name__)

    def onOpen(self):
        self.factory.instance = self

    def onConnect(self, response):
        self.logger.info("WsClientProtocol execute onConnect")
        if self.payload:
            self.logger.info("WsClientProtocol will Send message to OKX Server")
            self.sendMessage(self.payload, isBinary=False)
        self.factory.resetDelay()

    def onMessage(self, payload, isBinary):
        self.logger.info("WsClientProtocol execute onMessage begin")
        if not isBinary:
            try:
                payload_obj = json.loads(payload.decode("utf8"))
            except Exception as e:
                self.logger.error("WsClientProtocol onMessage error;e:{}".format(e))
            else:
                self.factory.callback(payload_obj)

    def onClose(self, wasClean, code, reason):
        self.logger.info(
            "WsClientProtocol WS connection will be closed; wasClean={0}, code={1}, reason: {2}".format(wasClean, code,
                                                                                                        reason))

    def onPing(self, payload):
        self.logger.info("WsClientProtocol execute onPing")
        self.sendPong()
        self.logger.info("WsClientProtocol execute onPing finish")

    def onPong(self, payload):
        self.logger.info("WsClientProtocol execute onPong")
