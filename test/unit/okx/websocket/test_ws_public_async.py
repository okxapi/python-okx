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

# Test constants
TEST_WS_URL = 'wss://test.example.com'
MOCK_WS_FACTORY = 'okx.websocket.WsPublicAsync.WebSocketFactory'

# Placeholder client identifiers for constructing the websocket client in unit
# tests. The WebSocketFactory is mocked, so these dummy strings are never signed
# or sent over a real connection — they are not real credentials.
_STUB_ID = "test_api_key"
_STUB_SIGN = "test_secret_key"
_STUB_PHRASE = "test_passphrase"


class TestWsPublicAsyncInit(unittest.TestCase):
    """Unit tests for WsPublicAsync initialization"""

    def test_init_with_url(self):
        """Test initialization with url parameter"""
        with patch.object(ws_public_module, 'WebSocketFactory') as mock_factory:
            ws = WsPublicAsync(url=TEST_WS_URL)

            self.assertEqual(ws.url, TEST_WS_URL)
            self.assertEqual(ws.apiKey, '')
            self.assertEqual(ws.passphrase, '')
            self.assertEqual(ws.secretKey, '')
            self.assertFalse(ws.debug)
            self.assertFalse(ws.isLoggedIn)

    def test_init_with_credentials(self):
        """Test initialization with all credentials for business channel"""
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(
                url=TEST_WS_URL,
                apiKey=_STUB_ID,
                passphrase=_STUB_PHRASE,
                secretKey=_STUB_SIGN
            )

            self.assertEqual(ws.apiKey, _STUB_ID)
            self.assertEqual(ws.passphrase, _STUB_PHRASE)
            self.assertEqual(ws.secretKey, _STUB_SIGN)

    def test_init_with_debug_enabled(self):
        """Test initialization with debug mode enabled"""
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL, debug=True)

            self.assertTrue(ws.debug)

    def test_init_with_debug_disabled(self):
        """Test initialization with debug mode disabled (default)"""
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL, debug=False)

            self.assertFalse(ws.debug)


class TestWsPublicAsyncLogin(unittest.TestCase):
    """Unit tests for WsPublicAsync login method"""

    def test_login_without_credentials_raises_error(self):
        """Test that login raises ValueError when credentials are missing"""
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL)

            async def run_test():
                with self.assertRaises(ValueError) as context:
                    await ws.login()
                self.assertIn("apiKey, secretKey and passphrase are required for login", str(context.exception))

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_login_with_credentials_success(self):
        """Test successful login with valid credentials"""
        with patch(MOCK_WS_FACTORY) as mock_factory, \
             patch('okx.websocket.WsPublicAsync.WsUtils.initLoginParams') as mock_init_login:

            mock_init_login.return_value = '{"op":"login","args":[...]}'

            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(
                url=TEST_WS_URL,
                apiKey=_STUB_ID,
                passphrase=_STUB_PHRASE,
                secretKey=_STUB_SIGN
            )
            mock_websocket = AsyncMock()
            ws.websocket = mock_websocket

            async def run_test():
                result = await ws.login()
                self.assertTrue(result)
                self.assertTrue(ws.isLoggedIn)
                mock_init_login.assert_called_once_with(
                    useServerTime=False,
                    apiKey=_STUB_ID,
                    passphrase=_STUB_PHRASE,
                    secretKey=_STUB_SIGN
                )
                mock_websocket.send.assert_called_once()

            asyncio.get_event_loop().run_until_complete(run_test())


class TestWsPublicAsyncSubscribe(unittest.TestCase):
    """Unit tests for WsPublicAsync subscribe method"""

    def test_subscribe_without_id(self):
        """Test subscribe without id parameter"""
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL)
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
            ws = WsPublicAsync(url=TEST_WS_URL)
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
            ws = WsPublicAsync(url=TEST_WS_URL)
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
            ws = WsPublicAsync(url=TEST_WS_URL)
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
            ws = WsPublicAsync(url=TEST_WS_URL)
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
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL)
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
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL)
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
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL)
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
        with patch(MOCK_WS_FACTORY):
            from okx.websocket.WsPublicAsync import WsPublicAsync
            ws = WsPublicAsync(url=TEST_WS_URL)
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

            ws = WsPublicAsync(url=TEST_WS_URL)

            async def run_test():
                await ws.stop()
                mock_factory_instance.close.assert_called_once()

            asyncio.get_event_loop().run_until_complete(run_test())

    def test_start_returns_task(self):
        """start() returns the consume task so the caller can retain/await it (GH#116)"""
        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url=TEST_WS_URL)

            async def run_test():
                ws.connect = AsyncMock()
                ws.consume = AsyncMock()
                task = await ws.start()
                self.assertIsInstance(task, asyncio.Task)
                await task

            asyncio.get_event_loop().run_until_complete(run_test())


class _RaisingAsyncIterator:
    """Async iterator that yields queued messages then raises the given exception."""

    def __init__(self, exc, messages=None):
        self._messages = list(messages or [])
        self._exc = exc

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._messages:
            return self._messages.pop(0)
        raise self._exc


class TestWsPublicAsyncConsumeErrorPropagation(unittest.TestCase):
    """Unit tests for consume() ConnectionClosedError handling (GH#116)"""

    def test_consume_propagates_connection_closed_and_pushes_error_event(self):
        """A dropped socket reaches the callback as an error event and re-raises"""
        from websockets.exceptions import ConnectionClosedError

        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url=TEST_WS_URL)
            received = []
            ws.callback = received.append
            exc = ConnectionClosedError(None, None)
            ws.websocket = _RaisingAsyncIterator(exc, messages=['{"data": "ok"}'])

            async def run_test():
                with self.assertRaises(ConnectionClosedError):
                    await ws.consume()

            with patch.object(ws_public_module.logger, 'error') as mock_log_error:
                asyncio.get_event_loop().run_until_complete(run_test())
                mock_log_error.assert_called_once()

            # Normal message delivered first, then the injected error event
            self.assertEqual(received[0], '{"data": "ok"}')
            error_payload = json.loads(received[1])
            self.assertEqual(error_payload["event"], "error")
            self.assertEqual(error_payload["code"], "ConnClosed")

    def test_consume_happy_path_unchanged(self):
        """Normal messages still reach the callback with no error event"""
        with patch.object(ws_public_module, 'WebSocketFactory'):
            ws = WsPublicAsync(url=TEST_WS_URL)
            received = []
            ws.callback = received.append

            class _CleanIterator:
                def __init__(self, messages):
                    self._messages = list(messages)

                def __aiter__(self):
                    return self

                async def __anext__(self):
                    if self._messages:
                        return self._messages.pop(0)
                    raise StopAsyncIteration

            ws.websocket = _CleanIterator(['a', 'b'])

            async def run_test():
                await ws.consume()

            asyncio.get_event_loop().run_until_complete(run_test())
            self.assertEqual(received, ['a', 'b'])


if __name__ == '__main__':
    unittest.main()
