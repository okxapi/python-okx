import asyncio
import json
import logging

from okx.websocket.WebSocketFactory import WebSocketFactory

logger = logging.getLogger(__name__)


class WsPublicAsync:
    def __init__(self, url):
        self.url = url
        self.subscriptions = set()
        self.callback = None
        self.loop = asyncio.get_event_loop()
        self.factory = WebSocketFactory(url)
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
        payload_dict = {
            "op": "subscribe",
            "args": params
        }
        if id is not None:
            payload_dict["id"] = id
        payload = json.dumps(payload_dict)
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
        logger.info(f"unsubscribe: {payload}")
        await self.websocket.send(payload)

    async def stop(self):
        await self.factory.close()

    async def start(self):
        logger.info("Connecting to WebSocket...")
        await self.connect()
        self.loop.create_task(self.consume())

    def stop_sync(self):
        self.loop.run_until_complete(self.stop())
