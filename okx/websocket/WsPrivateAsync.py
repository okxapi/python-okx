import asyncio
import json
import logging
import warnings

from okx.websocket import WsUtils
from okx.websocket.WebSocketFactory import WebSocketFactory

logger = logging.getLogger(__name__)


class WsPrivateAsync:
    def __init__(self, apiKey, passphrase, secretKey, url, useServerTime=None, debug=False):
        self.url = url
        self.subscriptions = set()
        self.callback = None
        self.loop = asyncio.get_event_loop()
        self.factory = WebSocketFactory(url)
        self.apiKey = apiKey
        self.passphrase = passphrase
        self.secretKey = secretKey
        self.useServerTime = False
        self.websocket = None
        self.debug = debug

        # Set log level
        if debug:
            logger.setLevel(logging.DEBUG)

        # Deprecation warning for useServerTime parameter
        if useServerTime is not None:
            warnings.warn("useServerTime parameter is deprecated. Please remove it.", DeprecationWarning)

    async def connect(self):
        self.websocket = await self.factory.connect()

    async def consume(self):
        async for message in self.websocket:
            if self.debug:
                logger.debug("Received message: {%s}", message)
            if self.callback:
                self.callback(message)

    async def subscribe(self, params: list, callback, id: str = None):
        self.callback = callback

        logRes = await self.login()
        await asyncio.sleep(5)
        if logRes:
            payload_dict = {
                "op": "subscribe",
                "args": params
            }
            if id is not None:
                payload_dict["id"] = id
            payload = json.dumps(payload_dict)
            if self.debug:
                logger.debug(f"subscribe: {payload}")
            await self.websocket.send(payload)
        # await self.consume()

    async def login(self):
        loginPayload = WsUtils.initLoginParams(
            useServerTime=self.useServerTime,
            apiKey=self.apiKey,
            passphrase=self.passphrase,
            secretKey=self.secretKey
        )
        if self.debug:
            logger.debug(f"login: {loginPayload}")
        await self.websocket.send(loginPayload)
        return True

    async def unsubscribe(self, params: list, callback, id: str = None):
        self.callback = callback
        payload_dict = {
            "op": "unsubscribe",
            "args": params
        }
        if id is not None:
            payload_dict["id"] = id
        payload = json.dumps(payload_dict)
        if self.debug:
            logger.debug(f"unsubscribe: {payload}")
        else:
            logger.info(f"unsubscribe: {payload}")
        await self.websocket.send(payload)

    async def send(self, op: str, args: list, callback=None, id: str = None):
        """
        Generic send method
        :param op: Operation type
        :param args: Parameter list
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        payload_dict = {
            "op": op,
            "args": args
        }
        if id is not None:
            payload_dict["id"] = id
        payload = json.dumps(payload_dict)
        if self.debug:
            logger.debug(f"send: {payload}")
        await self.websocket.send(payload)

    async def place_order(self, args: list, callback=None, id: str = None):
        """
        Place order
        :param args: Order parameter list
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        await self.send("order", args, id=id)

    async def batch_orders(self, args: list, callback=None, id: str = None):
        """
        Batch place orders
        :param args: Batch order parameter list
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        await self.send("batch-orders", args, id=id)

    async def cancel_order(self, args: list, callback=None, id: str = None):
        """
        Cancel order
        :param args: Cancel order parameter list
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        await self.send("cancel-order", args, id=id)

    async def batch_cancel_orders(self, args: list, callback=None, id: str = None):
        """
        Batch cancel orders
        :param args: Batch cancel order parameter list
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        await self.send("batch-cancel-orders", args, id=id)

    async def amend_order(self, args: list, callback=None, id: str = None):
        """
        Amend order
        :param args: Amend order parameter list
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        await self.send("amend-order", args, id=id)

    async def batch_amend_orders(self, args: list, callback=None, id: str = None):
        """
        Batch amend orders
        :param args: Batch amend order parameter list
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        await self.send("batch-amend-orders", args, id=id)

    async def mass_cancel(self, args: list, callback=None, id: str = None):
        """
        Mass cancel orders
        Note: This method is for /ws/v5/business channel, rate limit: 1 request/second
        :param args: Cancel parameter list, contains instType and instFamily
        :param callback: Callback function
        :param id: Optional request ID
        """
        if callback:
            self.callback = callback
        await self.send("mass-cancel", args, id=id)

    async def stop(self):
        await self.factory.close()

    async def start(self):
        if self.debug:
            logger.debug("Connecting to WebSocket...")
        else:
            logger.info("Connecting to WebSocket...")
        await self.connect()
        self.loop.create_task(self.consume())

    def stop_sync(self):
        if self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.stop(), self.loop)
            future.result(timeout=10)
        else:
            self.loop.run_until_complete(self.stop())
