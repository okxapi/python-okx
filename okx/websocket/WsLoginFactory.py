# import time
#
# import WsUtils
# from WsClientProtocol import *
# from autobahn.twisted.websocket import WebSocketClientFactory
# from twisted.internet.protocol import ReconnectingClientFactory
#
#
# class WsReconnectingClientFactory(ReconnectingClientFactory):
#     """
#         @ivar maxDelay: Maximum number of seconds between connection attempts.
#         @ivar initialDelay: Delay for the first reconnection attempt.
#         @ivar maxRetries: Maximum number of consecutive unsuccessful connection
#             attempts, after which no further connection attempts will be made. If
#             this is not explicitly set, no maximum is applied.
#         """
#     initialDelay = 0.1
#     maxDelay = 1
#     maxRetries = 4
#
#
# class WsLoginFactory(WebSocketClientFactory, WsReconnectingClientFactory):
#     reachMaxRetriesError = {"e": "error", "m": "reached max connect retries"}
#
#     def __init__(self, *args, useServerTime: str, apiKey: str, passphrase: str, secretKey: str, **kwargs):
#         WebSocketClientFactory.__init__(self, *args, **kwargs)
#         self.apiKey = apiKey
#         self.passphrase = passphrase
#         self.secretKey = secretKey
#         self.useServerTime = useServerTime
#         self.instance = None
#         self.preTime = time.time()
#         self.logger = logging.getLogger(__name__)
#
#     def startedConnecting(self, connector):
#         self.logger.info("WsClientFactory execute startedConnecting")
#
#     def clientConnectionFailed(self, connector, reason):
#         self.logger.error(
#             "Can't connect to server. Reason: {}. Retrying: {}".format(reason, self.retries + 1))
#         self.retry(connector)
#         if self.retries > self.maxRetries:
#             self.callback(self.reachMaxRetriesError)
#
#     def clientConnectionLost(self, connector, reason):
#         cur = time.time()
#         print("WsClientFactory,pre team=", cur - self.preTime)
#         self.preTime = cur
#         self.logger.error("WsClientFactory execute clientConnectionLost. Reason: {},retried {} times".format(reason,
#                                                                                                              self.retries + 1))
#         self.retry(connector)
#         if self.retries > self.maxRetries:
#             self.callback(self.reachMaxRetriesError)
#
#     def buildProtocol(self, addr):
#         payload = WsUtils.initLoginParams(useServerTime=self.useServerTime, apiKey=self.apiKey,
#                                           passphrase=self.passphrase, secretKey=self.secretKey)
#         protocol = WsClientProtocol(self, payload=payload)
#         return protocol
