"""
Unit tests for okx.okxclient module

Mirrors the structure: okx/okxclient.py -> test/unit/okx/test_okxclient.py
"""
import unittest
import warnings
from unittest.mock import patch, MagicMock

# Test constants
MOCK_CLIENT_INIT = 'okx.okxclient.Client.__init__'
TEST_PROXY_URL = 'http://proxy.example.com:8080'
TEST_API_ENDPOINT = '/api/v5/test'


class TestOkxClientInit(unittest.TestCase):
    """Unit tests for OkxClient initialization"""

    def test_init_with_default_parameters(self):
        """Test initialization with default parameters"""
        with patch(MOCK_CLIENT_INIT) as mock_init:
            mock_init.return_value = None
            
            from okx.okxclient import OkxClient
            client = OkxClient()

            self.assertEqual(client.API_KEY, '-1')
            self.assertEqual(client.API_SECRET_KEY, '-1')
            self.assertEqual(client.PASSPHRASE, '-1')
            self.assertEqual(client.flag, '1')
            self.assertFalse(client.debug)

    def test_init_with_custom_parameters(self):
        """Test initialization with custom parameters"""
        with patch(MOCK_CLIENT_INIT) as mock_init:
            mock_init.return_value = None
            
            from okx.okxclient import OkxClient
            client = OkxClient(
                api_key='test_key',
                api_secret_key='test_secret',
                passphrase='test_pass',
                flag='0',
                debug=True
            )

            self.assertEqual(client.API_KEY, 'test_key')
            self.assertEqual(client.API_SECRET_KEY, 'test_secret')
            self.assertEqual(client.PASSPHRASE, 'test_pass')
            self.assertEqual(client.flag, '0')
            self.assertTrue(client.debug)

    def test_init_with_deprecated_use_server_time_shows_warning(self):
        """Test that using deprecated use_server_time parameter shows warning"""
        with patch(MOCK_CLIENT_INIT) as mock_init:
            mock_init.return_value = None
            
            from okx.okxclient import OkxClient
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                client = OkxClient(use_server_time=True)

                self.assertEqual(len(w), 1)
                self.assertTrue(issubclass(w[0].category, DeprecationWarning))
                self.assertIn("use_server_time parameter is deprecated", str(w[0].message))


class TestOkxClientHttpxCompatibility(unittest.TestCase):
    """Unit tests for httpx version compatibility in OkxClient"""

    def test_init_with_new_httpx_proxy_parameter(self):
        """Test initialization with new httpx version using proxy parameter"""
        with patch(MOCK_CLIENT_INIT) as mock_init:
            # Simulate new httpx version (accepts proxy parameter)
            mock_init.return_value = None
            
            from okx.okxclient import OkxClient
            client = OkxClient(proxy=TEST_PROXY_URL)

            # Should call super().__init__ with proxy parameter
            mock_init.assert_called_once()
            call_kwargs = mock_init.call_args
            self.assertIn('proxy', call_kwargs.kwargs)
            self.assertEqual(call_kwargs.kwargs['proxy'], TEST_PROXY_URL)

    def test_init_with_old_httpx_falls_back_to_proxies(self):
        """Test initialization falls back to proxies for old httpx version"""
        call_count = [0]
        
        def mock_init_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1 and 'proxy' in kwargs:
                # First call with proxy parameter - simulate old httpx raising TypeError
                raise TypeError("__init__() got an unexpected keyword argument 'proxy'")
            # Second call should work (with proxies or without)
            return None

        with patch(MOCK_CLIENT_INIT) as mock_init:
            mock_init.side_effect = mock_init_side_effect
            
            from okx.okxclient import OkxClient
            client = OkxClient(proxy=TEST_PROXY_URL)

            # Should have been called twice
            self.assertEqual(mock_init.call_count, 2)
            
            # Second call should use proxies parameter
            second_call = mock_init.call_args_list[1]
            self.assertIn('proxies', second_call.kwargs)
            expected_proxies = {
                'http://': TEST_PROXY_URL,
                'https://': TEST_PROXY_URL
            }
            self.assertEqual(second_call.kwargs['proxies'], expected_proxies)

    def test_init_with_old_httpx_no_proxy(self):
        """Test initialization with old httpx version without proxy"""
        call_count = [0]
        
        def mock_init_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1 and 'proxy' in kwargs:
                # First call with proxy parameter - simulate old httpx raising TypeError
                raise TypeError("__init__() got an unexpected keyword argument 'proxy'")
            return None

        with patch(MOCK_CLIENT_INIT) as mock_init:
            mock_init.side_effect = mock_init_side_effect
            
            from okx.okxclient import OkxClient
            client = OkxClient()  # No proxy

            # Should have been called twice
            self.assertEqual(mock_init.call_count, 2)
            
            # Second call should not have proxies parameter
            second_call = mock_init.call_args_list[1]
            self.assertNotIn('proxies', second_call.kwargs)

    def test_init_without_proxy(self):
        """Test initialization without proxy parameter"""
        with patch(MOCK_CLIENT_INIT) as mock_init:
            mock_init.return_value = None
            
            from okx.okxclient import OkxClient
            client = OkxClient()

            mock_init.assert_called_once()
            call_kwargs = mock_init.call_args.kwargs
            self.assertEqual(call_kwargs.get('proxy'), None)


class TestOkxClientRequest(unittest.TestCase):
    """Unit tests for OkxClient request methods"""

    def setUp(self):
        """Set up test fixtures"""
        with patch(MOCK_CLIENT_INIT) as mock_init:
            mock_init.return_value = None
            from okx.okxclient import OkxClient
            self.client = OkxClient(
                api_key='test_key',
                api_secret_key='test_secret',
                passphrase='test_pass',
                flag='0'
            )

    def test_request_without_params(self):
        """Test _request_without_params calls _request with empty dict"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'code': '0'}
            
            result = self.client._request_without_params('GET', TEST_API_ENDPOINT)
            
            mock_request.assert_called_once_with('GET', TEST_API_ENDPOINT, {})

    def test_request_with_params(self):
        """Test _request_with_params passes params correctly"""
        with patch.object(self.client, '_request') as mock_request:
            mock_request.return_value = {'code': '0'}
            params = {'instId': 'BTC-USDT'}
            
            result = self.client._request_with_params('GET', TEST_API_ENDPOINT, params)
            
            mock_request.assert_called_once_with('GET', TEST_API_ENDPOINT, params)


if __name__ == '__main__':
    unittest.main()

