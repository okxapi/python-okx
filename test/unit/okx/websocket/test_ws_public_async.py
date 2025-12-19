"""
Unit tests for okx.websocket.WsPublicAsync module

Mirrors the structure: okx/websocket/WsPublicAsync.py -> test/unit/okx/websocket/test_ws_public_async.py
"""
import json
import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Import the module first so patch can resolve the path
import okx.websocket.WsPublicAsync as ws_public_module
from okx.websocket.WsPublicAsync import WsPublicAsync


class TestWsPublicAsyncInit(unittest.TestCase):
    """Unit tests for WsPublicAsync initialization"""

    def test_init_with_url(self):
        """Test initialization with url parameter"""
        with patch.object(ws_public_module, 'WebSocketFactory') as mock_factory:
            ws = WsPublicAsync(url="wss://test.example.com")

            self.assertEqual(ws.url, "wss://test.example.com")
            self.assertIsNone(ws.callback)
            self.assertIsNone(ws.websocket)
            mock_factory.assert_called_once_with("wss://test.example.com")


class TestWsPublicAsyncSubscribe(unittest.TestCase):
    """Unit tests for WsPublicAsync subscribe method"""

    def test_subscribe_sets_callback(self):
        """Test subscribe sets callback correctly"""
        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "tickers", "instId": "BTC-USDT"}]

            async def run_test():
                await ws.subscribe(params, callback)
                self.assertEqual(ws.callback, callback)
                mock_websocket.send.assert_called_once()
                
                # Verify the payload
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "subscribe")
                self.assertEqual(payload["args"], params)
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_subscribe_with_id(self):
        """Test subscribe with id parameter"""
        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "tickers", "instId": "BTC-USDT"}]

            async def run_test():
                await ws.subscribe(params, callback, id="sub001")

                # Verify the payload includes id
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "subscribe")
                self.assertEqual(payload["args"], params)
                self.assertEqual(payload["id"], "sub001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_subscribe_with_multiple_channels(self):
        """Test subscribe with multiple channels"""
        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [
                {"channel": "tickers", "instId": "BTC-USDT"},
                {"channel": "tickers", "instId": "ETH-USDT"}
            ]

            async def run_test():
                await ws.subscribe(params, callback, id="multi001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(len(payload["args"]), 2)
                self.assertEqual(payload["id"], "multi001")

            asyncio.get_event_loop().run_until_complete(run_test())


class TestWsPublicAsyncUnsubscribe(unittest.TestCase):
    """Unit tests for WsPublicAsync unsubscribe method"""

    def test_unsubscribe_without_id(self):
        """Test unsubscribe without id parameter"""
        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "tickers", "instId": "BTC-USDT"}]

            async def run_test():
                await ws.unsubscribe(params, callback)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "unsubscribe")
                self.assertEqual(payload["args"], params)
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_unsubscribe_with_id(self):
        """Test unsubscribe with id parameter"""
        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "tickers", "instId": "BTC-USDT"}]

            async def run_test():
                await ws.unsubscribe(params, callback, id="unsub001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "unsubscribe")
                self.assertEqual(payload["id"], "unsub001")

            asyncio.get_event_loop().run_until_complete(run_test())


class TestWsPublicAsyncStartStop(unittest.TestCase):
    """Unit tests for WsPublicAsync start and stop methods"""

    def test_stop(self):
        """Test stop method closes the factory"""
        with patch.object(ws_public_module, 'WebSocketFactory') as mock_factory_class:
            mock_factory_instance = MagicMock()
            mock_factory_instance.close = AsyncMock()
            mock_factory_class.return_value = mock_factory_instance

            ws = WsPublicAsync(url="wss://test.example.com")

            async def run_test():
                await ws.stop()
                mock_factory_instance.close.assert_called_once()

            asyncio.get_event_loop().run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
