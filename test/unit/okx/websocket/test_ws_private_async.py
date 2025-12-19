"""
Unit tests for okx.websocket.WsPrivateAsync module

Mirrors the structure: okx/websocket/WsPrivateAsync.py -> test/unit/okx/websocket/test_ws_private_async.py
"""
import json
import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Import the module first so patch can resolve the path
import okx.websocket.WsPrivateAsync as ws_private_module
from okx.websocket.WsPrivateAsync import WsPrivateAsync


class TestWsPrivateAsyncInit(unittest.TestCase):
    """Unit tests for WsPrivateAsync initialization"""

    def test_init_with_required_params(self):
        """Test initialization with required parameters"""
        with patch.object(ws_private_module, 'WebSocketFactory') as mock_factory:
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                useServerTime=False
            )

            self.assertEqual(ws.apiKey, "test_api_key")
            self.assertEqual(ws.passphrase, "test_passphrase")
            self.assertEqual(ws.secretKey, "test_secret_key")
            self.assertEqual(ws.url, "wss://test.example.com")
            self.assertFalse(ws.useServerTime)
            mock_factory.assert_called_once_with("wss://test.example.com")


class TestWsPrivateAsyncSubscribe(unittest.TestCase):
    """Unit tests for WsPrivateAsync subscribe method"""

    def test_subscribe_sends_correct_payload(self):
        """Test subscribe sends correct payload after login"""
        with patch.object(ws_private_module, 'WebSocketFactory'), \
             patch.object(ws_private_module, 'WsUtils') as mock_ws_utils, \
             patch.object(ws_private_module.asyncio, 'sleep', new_callable=AsyncMock):
            
            mock_ws_utils.initLoginParams.return_value = '{"op":"login"}'
            
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                useServerTime=False
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "account", "ccy": "BTC"}]

            async def run_test():
                await ws.subscribe(params, callback)
                self.assertEqual(ws.callback, callback)
                # Second call should be the subscribe (first is login)
                subscribe_call = mock_websocket.send.call_args_list[1]
                payload = json.loads(subscribe_call[0][0])
                self.assertEqual(payload["op"], "subscribe")
                self.assertEqual(payload["args"], params)
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_subscribe_with_id(self):
        """Test subscribe with id parameter"""
        with patch.object(ws_private_module, 'WebSocketFactory'), \
             patch.object(ws_private_module, 'WsUtils') as mock_ws_utils, \
             patch.object(ws_private_module.asyncio, 'sleep', new_callable=AsyncMock):

            mock_ws_utils.initLoginParams.return_value = '{"op":"login"}'

            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                useServerTime=False
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "account", "ccy": "BTC"}]

            async def run_test():
                await ws.subscribe(params, callback, id="sub001")
                # Second call should be the subscribe (first is login)
                subscribe_call = mock_websocket.send.call_args_list[1]
                payload = json.loads(subscribe_call[0][0])
                self.assertEqual(payload["op"], "subscribe")
                self.assertEqual(payload["id"], "sub001")

            asyncio.get_event_loop().run_until_complete(run_test())


class TestWsPrivateAsyncUnsubscribe(unittest.TestCase):
    """Unit tests for WsPrivateAsync unsubscribe method"""

    def test_unsubscribe_sends_correct_payload(self):
        """Test unsubscribe sends correct payload"""
        with patch.object(ws_private_module, 'WebSocketFactory'):
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                useServerTime=False
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "account", "ccy": "BTC"}]

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
        with patch.object(ws_private_module, 'WebSocketFactory'):
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                useServerTime=False
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            callback = MagicMock()
            params = [{"channel": "account", "ccy": "BTC"}]

            async def run_test():
                await ws.unsubscribe(params, callback, id="unsub001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "unsubscribe")
                self.assertEqual(payload["id"], "unsub001")

            asyncio.get_event_loop().run_until_complete(run_test())


class TestWsPrivateAsyncLogin(unittest.TestCase):
    """Unit tests for WsPrivateAsync login method"""

    def test_login_calls_init_login_params(self):
        """Test login calls WsUtils.initLoginParams with correct parameters"""
        with patch.object(ws_private_module, 'WebSocketFactory'), \
             patch.object(ws_private_module, 'WsUtils') as mock_ws_utils:
            
            mock_ws_utils.initLoginParams.return_value = '{"op":"login","args":[...]}'
            
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                useServerTime=True
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket

            async def run_test():
                result = await ws.login()
                self.assertTrue(result)
                mock_ws_utils.initLoginParams.assert_called_once_with(
                    useServerTime=True,
                    apiKey="test_api_key",
                    passphrase="test_passphrase",
                    secretKey="test_secret_key"
                )

            asyncio.get_event_loop().run_until_complete(run_test())


class TestWsPrivateAsyncStartStop(unittest.TestCase):
    """Unit tests for WsPrivateAsync start and stop methods"""

    def test_stop(self):
        """Test stop method closes the factory"""
        with patch.object(ws_private_module, 'WebSocketFactory') as mock_factory_class:
            mock_factory_instance = MagicMock()
            mock_factory_instance.close = AsyncMock()
            mock_factory_class.return_value = mock_factory_instance

            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                useServerTime=False
            )

            async def run_test():
                await ws.stop()
                mock_factory_instance.close.assert_called_once()

            asyncio.get_event_loop().run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
