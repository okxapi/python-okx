"""
Unit tests for okx.MarketData MarketAPI.get_rpi_orderbook — TD 0.4.4 item #1
(GET /api/v5/market/books-rpi). Mirrors get_orderbook.
"""
import unittest
from unittest.mock import patch
from okx.MarketData import MarketAPI
from okx import consts as c

_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestGetRpiOrderbook(unittest.TestCase):
    def setUp(self):
        self.api = MarketAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0',
        )

    def test_books_rpi_constant_path(self):
        self.assertEqual(c.MARKET_BOOKS_RPI, '/api/v5/market/books-rpi')

    @patch.object(MarketAPI, '_request_with_params')
    def test_get_rpi_orderbook_required_only(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_rpi_orderbook(instId='BTC-USDT-SWAP')
        mock_request.assert_called_once_with(
            c.GET, c.MARKET_BOOKS_RPI, {'instId': 'BTC-USDT-SWAP', 'sz': ''})

    @patch.object(MarketAPI, '_request_with_params')
    def test_get_rpi_orderbook_with_sz(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_rpi_orderbook(instId='BTC-USDT-SWAP', sz='50')
        mock_request.assert_called_once_with(
            c.GET, c.MARKET_BOOKS_RPI, {'instId': 'BTC-USDT-SWAP', 'sz': '50'})


if __name__ == '__main__':
    unittest.main()
