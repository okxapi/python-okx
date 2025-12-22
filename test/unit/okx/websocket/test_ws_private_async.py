"""
Unit tests for okx.websocket.WsPrivateAsync module

Mirrors the structure: okx/websocket/WsPrivateAsync.py -> test/unit/okx/websocket/test_ws_private_async.py
"""
import json
import unittest
import asyncio
import warnings
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
                url="wss://test.example.com"
            )

            self.assertEqual(ws.apiKey, "test_api_key")
            self.assertEqual(ws.passphrase, "test_passphrase")
            self.assertEqual(ws.secretKey, "test_secret_key")
            self.assertEqual(ws.url, "wss://test.example.com")
            self.assertFalse(ws.useServerTime)
            self.assertFalse(ws.debug)
            mock_factory.assert_called_once_with("wss://test.example.com")

    def test_init_with_debug_enabled(self):
        """Test initialization with debug mode enabled"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            from okx.websocket.WsPrivateAsync import WsPrivateAsync
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com",
                debug=True
            )

            self.assertTrue(ws.debug)

    def test_init_with_deprecated_useServerTime_shows_warning(self):
        """Test that using deprecated useServerTime parameter shows warning"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            from okx.websocket.WsPrivateAsync import WsPrivateAsync

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                ws = WsPrivateAsync(
                    apiKey="test_api_key",
                    passphrase="test_passphrase",
                    secretKey="test_secret_key",
                    url="wss://test.example.com",
                    useServerTime=True
                )

                self.assertEqual(len(w), 1)
                self.assertTrue(issubclass(w[0].category, DeprecationWarning))
                self.assertIn("useServerTime parameter is deprecated", str(w[0].message))

    def test_init_without_useServerTime_no_warning(self):
        """Test that not using useServerTime parameter shows no warning"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            from okx.websocket.WsPrivateAsync import WsPrivateAsync

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                ws = WsPrivateAsync(
                    apiKey="test_api_key",
                    passphrase="test_passphrase",
                    secretKey="test_secret_key",
                    url="wss://test.example.com"
                )

                # No deprecation warning expected
                deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
                self.assertEqual(len(deprecation_warnings), 0)


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
                url="wss://test.example.com"
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
                url="wss://test.example.com"
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
                url="wss://test.example.com"
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
                url="wss://test.example.com"
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


class TestWsPrivateAsyncSend(unittest.TestCase):
    """Unit tests for WsPrivateAsync generic send method"""

    def test_send_without_id(self):
        """Test generic send method without id"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            from okx.websocket.WsPrivateAsync import WsPrivateAsync
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com"
            )
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
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            from okx.websocket.WsPrivateAsync import WsPrivateAsync
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com"
            )
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


class TestWsPrivateAsyncOrderMethods(unittest.TestCase):
    """Unit tests for WsPrivateAsync order-related methods"""

    def _create_ws_instance(self):
        """Helper to create WsPrivateAsync instance with mocked websocket"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            from okx.websocket.WsPrivateAsync import WsPrivateAsync
            ws = WsPrivateAsync(
                apiKey="test_api_key",
                passphrase="test_passphrase",
                secretKey="test_secret_key",
                url="wss://test.example.com"
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket
            return ws, mock_websocket

    def test_place_order_sends_correct_payload(self):
        """Test place_order sends correct operation"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            callback = MagicMock()
            order_args = [{
                "instId": "BTC-USDT",
                "tdMode": "cash",
                "side": "buy",
                "ordType": "limit",
                "sz": "0.001",
                "px": "30000"
            }]

            async def run_test():
                await ws.place_order(order_args, callback=callback, id="order001")
                self.assertEqual(ws.callback, callback)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "order")
                self.assertEqual(payload["args"], order_args)
                self.assertEqual(payload["id"], "order001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_place_order_without_id(self):
        """Test place_order without id parameter"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            order_args = [{"instId": "BTC-USDT"}]

            async def run_test():
                await ws.place_order(order_args)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "order")
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_batch_orders_sends_correct_payload(self):
        """Test batch_orders sends correct operation"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            callback = MagicMock()
            order_args = [
                {"instId": "BTC-USDT", "side": "buy", "sz": "0.001", "px": "30000"},
                {"instId": "ETH-USDT", "side": "buy", "sz": "0.01", "px": "2000"}
            ]

            async def run_test():
                await ws.batch_orders(order_args, callback=callback, id="batch001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "batch-orders")
                self.assertEqual(payload["args"], order_args)
                self.assertEqual(payload["id"], "batch001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_batch_orders_without_id(self):
        """Test batch_orders without id parameter"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            order_args = [{"instId": "BTC-USDT"}, {"instId": "ETH-USDT"}]

            async def run_test():
                await ws.batch_orders(order_args)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "batch-orders")
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_cancel_order_sends_correct_payload(self):
        """Test cancel_order sends correct operation"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            callback = MagicMock()
            cancel_args = [{"instId": "BTC-USDT", "ordId": "12345"}]

            async def run_test():
                await ws.cancel_order(cancel_args, callback=callback, id="cancel001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "cancel-order")
                self.assertEqual(payload["args"], cancel_args)
                self.assertEqual(payload["id"], "cancel001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_cancel_order_without_id(self):
        """Test cancel_order without id parameter"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            cancel_args = [{"instId": "BTC-USDT", "ordId": "12345"}]

            async def run_test():
                await ws.cancel_order(cancel_args)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "cancel-order")
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_batch_cancel_orders_sends_correct_payload(self):
        """Test batch_cancel_orders sends correct operation"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            callback = MagicMock()
            cancel_args = [
                {"instId": "BTC-USDT", "ordId": "12345"},
                {"instId": "ETH-USDT", "ordId": "67890"}
            ]

            async def run_test():
                await ws.batch_cancel_orders(cancel_args, callback=callback, id="batchCancel001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "batch-cancel-orders")
                self.assertEqual(payload["args"], cancel_args)
                self.assertEqual(payload["id"], "batchCancel001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_batch_cancel_orders_without_id(self):
        """Test batch_cancel_orders without id parameter"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            cancel_args = [{"instId": "BTC-USDT", "ordId": "12345"}]

            async def run_test():
                await ws.batch_cancel_orders(cancel_args)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "batch-cancel-orders")
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_amend_order_sends_correct_payload(self):
        """Test amend_order sends correct operation"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            callback = MagicMock()
            amend_args = [{
                "instId": "BTC-USDT",
                "ordId": "12345",
                "newSz": "0.002",
                "newPx": "31000"
            }]

            async def run_test():
                await ws.amend_order(amend_args, callback=callback, id="amend001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "amend-order")
                self.assertEqual(payload["args"], amend_args)
                self.assertEqual(payload["id"], "amend001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_amend_order_without_id(self):
        """Test amend_order without id parameter"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            amend_args = [{"instId": "BTC-USDT", "ordId": "12345", "newSz": "0.002"}]

            async def run_test():
                await ws.amend_order(amend_args)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "amend-order")
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_batch_amend_orders_sends_correct_payload(self):
        """Test batch_amend_orders sends correct operation"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            callback = MagicMock()
            amend_args = [
                {"instId": "BTC-USDT", "ordId": "12345", "newSz": "0.002"},
                {"instId": "ETH-USDT", "ordId": "67890", "newPx": "2100"}
            ]

            async def run_test():
                await ws.batch_amend_orders(amend_args, callback=callback, id="batchAmend001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "batch-amend-orders")
                self.assertEqual(payload["args"], amend_args)
                self.assertEqual(payload["id"], "batchAmend001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_batch_amend_orders_without_id(self):
        """Test batch_amend_orders without id parameter"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            amend_args = [{"instId": "BTC-USDT", "ordId": "12345", "newSz": "0.002"}]

            async def run_test():
                await ws.batch_amend_orders(amend_args)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "batch-amend-orders")
                self.assertNotIn("id", payload)

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_mass_cancel_sends_correct_payload(self):
        """Test mass_cancel sends correct operation"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            callback = MagicMock()
            mass_cancel_args = [{
                "instType": "SPOT",
                "instFamily": "BTC-USDT"
            }]

            async def run_test():
                await ws.mass_cancel(mass_cancel_args, callback=callback, id="massCancel001")
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "mass-cancel")
                self.assertEqual(payload["args"], mass_cancel_args)
                self.assertEqual(payload["id"], "massCancel001")

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_mass_cancel_without_id(self):
        """Test mass_cancel without id parameter"""
        with patch('okx.websocket.WsPrivateAsync.WebSocketFactory'):
            ws, mock_websocket = self._create_ws_instance()
            mass_cancel_args = [{"instType": "SPOT", "instFamily": "BTC-USDT"}]

            async def run_test():
                await ws.mass_cancel(mass_cancel_args)
                call_args = mock_websocket.send.call_args[0][0]
                payload = json.loads(call_args)
                self.assertEqual(payload["op"], "mass-cancel")
                self.assertNotIn("id", payload)

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
                url="wss://test.example.com"
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket

            async def run_test():
                result = await ws.login()
                self.assertTrue(result)
                mock_ws_utils.initLoginParams.assert_called_once_with(
                    useServerTime=False,
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
                url="wss://test.example.com"
            )

            async def run_test():
                await ws.stop()
                mock_factory_instance.close.assert_called_once()

            asyncio.get_event_loop().run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
