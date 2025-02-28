import asyncio
import logging
import ssl

import certifi
import websockets

logger = logging.getLogger(__name__)


class WebSocketFactory:

    def __init__(self, url):
        self.url = url
        self.websocket = None
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        try:
            self.websocket = await websockets.connect(self.url, ssl=ssl_context)
            logger.info("WebSocket connection established.")
            return self.websocket
        except Exception as e:
            logger.error(f"Error connecting to WebSocket: {e}")
            return None

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
