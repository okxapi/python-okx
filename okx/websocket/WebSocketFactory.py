import logging
import ssl

import certifi
import websockets

logger = logging.getLogger(__name__)


class WebSocketFactory:

    def __init__(self, url, proxy=None):
        self.url = url
        self.proxy = proxy
        self.websocket = None

    async def connect(self):
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        try:
            connect_kwargs = {"ssl": ssl_context}
            if self.proxy is not None:
                connect_kwargs["proxy"] = self.proxy
            self.websocket = await websockets.connect(self.url, **connect_kwargs)
            logger.info("WebSocket connection established.")
            return self.websocket
        except Exception as e:
            logger.error(f"Error connecting to WebSocket: {e}")
            raise

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
