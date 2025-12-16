import asyncio
import json
import logging

from okx.websocket import WsUtils
from okx.websocket.WebSocketFactory import WebSocketFactory

logger = logging.getLogger(__name__)


class WsPrivateAsync:
    def __init__(self, apiKey, passphrase, secretKey, url, useServerTime):
        self.url = url
        self.subscriptions = set()
        self.callback = None
        self.loop = asyncio.get_event_loop()
        self.factory = WebSocketFactory(url)
        self.apiKey = apiKey
        self.passphrase = passphrase
        self.secretKey = secretKey
        self.useServerTime = useServerTime
        self.websocket = None

    async def connect(self):
        self.websocket = await self.factory.connect()

    async def consume(self):
        async for message in self.websocket:
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
            await self.websocket.send(payload)
        # await self.consume()

    async def login(self):
        loginPayload = WsUtils.initLoginParams(
            useServerTime=self.useServerTime,
            apiKey=self.apiKey,
            passphrase=self.passphrase,
            secretKey=self.secretKey
        )
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
        logger.info(f"unsubscribe: {payload}")
        await self.websocket.send(payload)
        # for param in params:
        #     self.subscriptions.discard(param)

    async def stop(self):
        await self.factory.close()

    async def start(self):
        logger.info("Connecting to WebSocket...")
        await self.connect()
        self.loop.create_task(self.consume())

    def stop_sync(self):
        self.loop.run_until_complete(self.stop())
