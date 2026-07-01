"""
Unit tests for okx.Trade module

Mirrors the structure: okx/Trade.py -> test/unit/okx/test_trade.py
"""
import unittest
from unittest.mock import patch
from okx.Trade import TradeAPI
from okx import consts as c

# Test constants
SAMPLE_ORDERS = [{'instId': 'BTC-USDT', 'algoId': '590xxxx'}]

# Placeholder client identifiers for constructing the API client in unit tests.
# Every request is mocked (see @patch.object below), so these dummy strings are
# never signed or transmitted — they are not real credentials.
_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestTradeAPICancelAlgoOrder(unittest.TestCase):
    """Unit tests for cancel_algo_order backward-compatible signature (GH#115)"""

    def setUp(self):
        """Set up test fixtures"""
        self.trade_api = TradeAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0'
        )

    @patch.object(TradeAPI, '_request_with_params')
    def test_cancel_algo_order_positional(self, mock_request):
        """New name: positional caller binds to orders_data (backward compatible)"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        result = self.trade_api.cancel_algo_order(SAMPLE_ORDERS)

        mock_request.assert_called_once_with(c.POST, c.CANCEL_ALGOS, SAMPLE_ORDERS)
        self.assertEqual(result, mock_response)

    @patch.object(TradeAPI, '_request_with_params')
    def test_cancel_algo_order_orders_data_keyword(self, mock_request):
        """orders_data keyword works"""
        mock_request.return_value = {'code': '0', 'msg': '', 'data': []}

        self.trade_api.cancel_algo_order(orders_data=SAMPLE_ORDERS)

        mock_request.assert_called_once_with(c.POST, c.CANCEL_ALGOS, SAMPLE_ORDERS)

    @patch.object(TradeAPI, '_request_with_params')
    def test_cancel_algo_order_params_keyword_alias(self, mock_request):
        """Legacy params= keyword still resolves via the deprecated alias (GH#115)"""
        mock_request.return_value = {'code': '0', 'msg': '', 'data': []}

        self.trade_api.cancel_algo_order(params=SAMPLE_ORDERS)

        mock_request.assert_called_once_with(c.POST, c.CANCEL_ALGOS, SAMPLE_ORDERS)

    @patch.object(TradeAPI, '_request_with_params')
    def test_cancel_algo_order_orders_data_takes_precedence(self, mock_request):
        """When both provided, orders_data wins over the legacy alias"""
        mock_request.return_value = {'code': '0', 'msg': '', 'data': []}
        legacy = [{'instId': 'ETH-USDT', 'algoId': '111'}]

        self.trade_api.cancel_algo_order(orders_data=SAMPLE_ORDERS, params=legacy)

        mock_request.assert_called_once_with(c.POST, c.CANCEL_ALGOS, SAMPLE_ORDERS)

    def test_cancel_algo_order_missing_data_raises(self):
        """No data supplied raises a clear ValueError"""
        with self.assertRaises(ValueError):
            self.trade_api.cancel_algo_order()

    def test_cancel_algo_order_has_docstring(self):
        """Method is documented (GH#115 discoverability)"""
        self.assertIsNotNone(TradeAPI.cancel_algo_order.__doc__)
        self.assertIn('orders_data', TradeAPI.cancel_algo_order.__doc__)


if __name__ == '__main__':
    unittest.main()
