"""Unit tests for the WebSocket transport factory."""

import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from okx.websocket.WebSocketFactory import WebSocketFactory


TEST_WS_URL = "wss://test.example.com/ws/v5/public"


class TestWebSocketFactory(unittest.TestCase):

    def test_connect_forwards_explicit_proxy(self):
        websocket = AsyncMock()

        async def run_test():
            with patch(
                "okx.websocket.WebSocketFactory.websockets.connect",
                new_callable=AsyncMock,
                return_value=websocket,
            ) as connect:
                factory = WebSocketFactory(TEST_WS_URL, proxy="http://127.0.0.1:7890")

                result = await factory.connect()

                self.assertIs(result, websocket)
                self.assertEqual(connect.await_args.args, (TEST_WS_URL,))
                self.assertEqual(connect.await_args.kwargs["proxy"], "http://127.0.0.1:7890")
                self.assertIn("ssl", connect.await_args.kwargs)

        asyncio.run(run_test())

    def test_connect_omits_proxy_when_not_configured(self):
        websocket = AsyncMock()

        async def run_test():
            with patch(
                "okx.websocket.WebSocketFactory.websockets.connect",
                new_callable=AsyncMock,
                return_value=websocket,
            ) as connect:
                factory = WebSocketFactory(TEST_WS_URL)

                await factory.connect()

                self.assertNotIn("proxy", connect.await_args.kwargs)

        asyncio.run(run_test())

    def test_connect_propagates_original_exception(self):
        error = OSError("proxy connection failed")

        async def run_test():
            with patch(
                "okx.websocket.WebSocketFactory.websockets.connect",
                new_callable=AsyncMock,
                side_effect=error,
            ):
                factory = WebSocketFactory(TEST_WS_URL)

                with self.assertRaises(OSError) as raised:
                    await factory.connect()

                self.assertIs(raised.exception, error)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
