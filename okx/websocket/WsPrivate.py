
from twisted.internet import reactor

from . import WsUtils
from .WsConnectManager import WsConnectManager


class WsPrivate(WsConnectManager):
    def __init__(self, apiKey: str, passphrase: str, secretKey: str, url: str, useServerTime: False):
        if ~WsUtils.isNotBlankStr(apiKey) or ~WsUtils.isNotBlankStr(passphrase) or ~WsUtils.isNotBlankStr(
                secretKey) or ~WsUtils.isNotBlankStr(url):
            return
        super().__init__(url, isPrivate=True)
        self.apiKey = apiKey
        self.passphrase = passphrase
        self.secretKey = secretKey
        self.useServerTime = useServerTime

    def subscribe(self, params: list, callback):
        self.subscribeSocket(params, callback)

    def unsubscribe(self, params: list, callback):
        self.unsubscribeSocket(params, callback)

    def stop(self):
        try:
            self.close()
        finally:
            reactor.stop()

