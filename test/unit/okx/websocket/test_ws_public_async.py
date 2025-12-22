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
            self.assertEqual(ws.apiKey, '')
            self.assertEqual(ws.passphrase, '')
            self.assertEqual(ws.secretKey, '')
            self.assertFalse(ws.debug)
            self.assertFalse(ws.isLoggedIn)

    def test_init_with_credentials(self):
        """Test initialization with all credentials for business channel"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(
                url="wss://test.example.com",
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key"
            )

            self.assertEqual(ws.apiKey, "test_api_key")
            self.assertEqual(ws.passphrase, "test_passphrase")
            self.assertEqual(ws.secretKey, "test_secret_key")

    def test_init_with_debug_enabled(self):
        """Test initialization with debug mode enabled"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url="wss://test.example.com", debug=True)

            self.assertTrue(ws.debug)

    def test_init_with_debug_disabled(self):
        """Test initialization with debug mode disabled (default)"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url="wss://test.example.com", debug=False)

            self.assertFalse(ws.debug)


class TestWsPublicAsyncLogin(unittest.TestCase):
    """Unit tests for WsPublicAsync login method"""

    def test_login_without_credentials_raises_error(self):
        """Test that login raises ValueError when credentials are missing"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url="wss://test.example.com")

            async def run_test():
                with self.assertRaises(ValueError) as context:
                    await ws.login()
                self.assertIn("apiKey, secretKey and passphrase are required for login", str(context.exception))

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_login_with_credentials_success(self):
        """Test successful login with valid credentials"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory') as mock_factory, \
             patch('okx.websocket.WsPublicAsync.WsUtils.initLoginParams') as mock_init_login:

            mock_init_login.return_value = '{"op":"login","args":[...]}'

            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(
                url="wss://test.example.com",
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key"
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket

            async def run_test():
                result = await ws.login()
                self.assertTrue(result)
                self.assertTrue(ws.isLoggedIn)
                mock_init_login.assert_called_once_with(
                    useServerTime=False,
                    apiKey="test_api_key",
                    passphrase="test_passphrase",
                    secretKey="test_secret_key"
                )
                mock_websocket.send.assert_called_once()

            asyncio.get_event_loop().run_until_complete(run_test())


class TestWsPublicAsyncSubscribe(unittest.TestCase):
    """Unit tests for WsPublicAsync subscribe method"""

    def test_subscribe_without_id(self):
        """Test subscribe without id parameter"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
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


class TestWsPublicAsyncSend(unittest.TestCase):
    """Unit tests for WsPublicAsync send method"""

    def test_send_without_id(self):
        """Test generic send method without id"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            args = [{"instId": "BTC-USDT"}]

            async def run_test():
                await ws.send("custom_op", args, callback=callback)
                self.assertEqual(ws.callback, callback)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "custom_op")
                self.assertEqual(payload["args"], args)
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_send_with_id(self):
        """Test generic send method with id"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            args = [{"instId": "BTC-USDT"}]

            async def run_test():
                await ws.send("custom_op", args, id="send001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "custom_op")
                self.assertEqual(payload["id"], "send001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_send_without_callback(self):
        """Test send method without callback (preserves existing callback)"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            existing_callback = MagicMock()
            ws.callback = existing_callback
            args = [{"instId": "BTC-USDT"}]

            async def run_test():
                await ws.send("custom_op", args)
                # Callback should remain unchanged
                self.assertEqual(ws.callback, existing_callback)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_send_with_new_callback_replaces_existing(self):
        """Test send method with new callback replaces existing callback"""
        with patch('okx.websocket.WsPublicAsync.WebSocketFactory'):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url="wss://test.example.com")
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            old_callback = MagicMock()
            new_callback = MagicMock()
            ws.callback = old_callback
            args = [{"instId": "BTC-USDT"}]

            async def run_test():
                await ws.send("custom_op", args, callback=new_callback)
                self.assertEqual(ws.callback, new_callback)

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
