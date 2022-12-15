from autobahn.twisted.websocket import WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory

from .WsClientProtocol import *


class WsReconnectingClientFactory(ReconnectingClientFactory):
    """
        @ivar maxDelay: Maximum number of seconds between connection attempts.
        @ivar initialDelay: Delay for the first reconnection attempt.
        @ivar maxRetries: Maximum number of consecutive unsuccessful connection
            attempts, after which no further connection attempts will be made. If
            this is not explicitly set, no maximum is applied.
        """
    initialDelay = 0.1
    maxDelay = 2
    maxRetries = 5


class WsClientFactory(WebSocketClientFactory, WsReconnectingClientFactory):
    reachMaxRetriesError = {"e": "error", "m": "reached max connect retries"}

    def __init__(self, *args, payload=None, **kwargs):
        WebSocketClientFactory.__init__(self, *args, **kwargs)
        self.instance = None
        self.subscribeSet = set()
        self.payload = payload
        self.logger = logging.getLogger(__name__)

    def startedConnecting(self, connector):
        self.logger.info("WsClientFactory execute startedConnecting")

    def clientConnectionFailed(self, connector, reason):
        self.logger.error(
            "Can't connect to server. Reason: {}. Retrying: {}".format(reason, self.retries + 1))
        self.retry(connector)
        if self.retries > self.maxRetries:
            self.callback(self.reachMaxRetriesError)

    def clientConnectionLost(self, connector, reason):
        self.logger.error("WsClientFactory execute clientConnectionLost. Reason: {},retried {} times".format(reason,
                                                                                                             self.retries + 1))
        self.retry(connector)
        if self.retries > self.maxRetries:
            self.callback(self.reachMaxRetriesError)

    def buildProtocol(self, addr):
        protocol = WsClientProtocol(self, payload=self.payload)
        return protocol
