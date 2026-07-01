import asyncio
import json
import logging

from websockets.exceptions import ConnectionClosedError

from okx.websocket import WsUtils
from okx.websocket.WebSocketFactory import WebSocketFactory

logger = logging.getLogger(__name__)


class WsPublicAsync:
    def __init__(self, url, apiKey='', passphrase='', secretKey='', debug=False):
        self.url = url
        self.subscriptions = set()
        self.callback = None
        self.loop = asyncio.get_event_loop()
        self.factory = WebSocketFactory(url)
        self.websocket = None
        self.debug = debug
        # Credentials for business channel login
        self.apiKey = apiKey
        self.passphrase = passphrase
        self.secretKey = secretKey
        self.isLoggedIn = False

        # Set log level
        if debug:
            logger.setLevel(logging.DEBUG)

    async def connect(self):
        self.websocket = await self.factory.connect()

    async def consume(self):
        try:
            async for message in self.websocket:
                if self.debug:
                    logger.debug("Received message: {%s}", message)
                if self.callback:
                    self.callback(message)
        except ConnectionClosedError as e:
            logger.error(f"WebSocket connection closed: {e}")
            if self.callback:
                self.callback(json.dumps({"event": "error", "code": "ConnClosed", "msg": str(e)}))
            raise

    async def login(self):
        """
        Login method for business channel that requires authentication (e.g. /ws/v5/business)
        """
        if not self.apiKey or not self.secretKey or not self.passphrase:
            raise ValueError("apiKey, secretKey and passphrase are required for login")

        loginPayload = WsUtils.initLoginParams(
            useServerTime=False,
            apiKey=self.apiKey,
            passphrase=self.passphrase,
            secretKey=self.secretKey
        )
        if self.debug:
            logger.debug(f"login: {loginPayload}")
        await self.websocket.send(loginPayload)
        self.isLoggedIn = True
        return True

    async def subscribe(self, params: list, callback, id: str = None):
        self.callback = callback
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

    async def stop(self):
        await self.factory.close()

    async def start(self):
        if self.debug:
            logger.debug("Connecting to WebSocket...")
        else:
            logger.info("Connecting to WebSocket...")
        await self.connect()
        return self.loop.create_task(self.consume())

    def stop_sync(self):
        if self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.stop(), self.loop)
            future.result(timeout=10)
        else:
            self.loop.run_until_complete(self.stop())
