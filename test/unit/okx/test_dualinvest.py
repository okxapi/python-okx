"""
Unit tests for okx.DualInvest DualInvestAPI — item #10 (8 endpoints).
"""
import unittest
from unittest.mock import patch
from okx.DualInvest import DualInvestAPI
from okx import consts as c

# Placeholder client identifiers — every request is mocked; not real credentials.
_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class _Base(unittest.TestCase):
    def setUp(self):
        self.api = DualInvestAPI(api_key=_STUB_ID, api_secret_key=_STUB_SIGN, passphrase=_STUB_PHRASE, flag='0')


class TestDualInvestNoParamGets(_Base):
    @patch.object(DualInvestAPI, '_request_without_params')
    def test_get_currency_pairs(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_currency_pairs()
        mock_request.assert_called_once_with(c.GET, c.DUAL_INVEST_CURRENCY_PAIRS)

    @patch.object(DualInvestAPI, '_request_without_params')
    def test_get_product_info(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_product_info()
        mock_request.assert_called_once_with(c.GET, c.DUAL_INVEST_PRODUCT_INFO)


class TestDualInvestParamMethods(_Base):
    @patch.object(DualInvestAPI, '_request_with_params')
    def test_request_quote(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.request_quote(ccy='BTC', investCcy='USDT', quoteCcy='USDT', side='buy', sz='1')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_REQUEST_QUOTE,
            {'ccy': 'BTC', 'investCcy': 'USDT', 'quoteCcy': 'USDT', 'side': 'buy', 'sz': '1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_trade(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.trade(quoteId='q1', ccy='BTC', investCcy='USDT', quoteCcy='USDT', side='buy', sz='1')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_TRADE,
            {'quoteId': 'q1', 'ccy': 'BTC', 'investCcy': 'USDT', 'quoteCcy': 'USDT', 'side': 'buy', 'sz': '1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_request_redeem_quote(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.request_redeem_quote(ordId='o1', ccy='BTC', sz='1')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_REQUEST_REDEEM_QUOTE, {'ordId': 'o1', 'ccy': 'BTC', 'sz': '1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_redeem(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.redeem(quoteId='q1', ordId='o1', ccy='BTC', sz='1')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_REDEEM, {'quoteId': 'q1', 'ordId': 'o1', 'ccy': 'BTC', 'sz': '1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_get_order_state(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_order_state(ordId='o1')
        mock_request.assert_called_once_with(c.GET, c.DUAL_INVEST_ORDER_STATE, {'ordId': 'o1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_get_order_history(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_order_history(ccy='BTC', after='1', before='2', limit='10')
        mock_request.assert_called_once_with(
            c.GET, c.DUAL_INVEST_ORDER_HISTORY,
            {'ccy': 'BTC', 'after': '1', 'before': '2', 'limit': '10'})


class TestDualInvestConstants(unittest.TestCase):
    def test_all_eight_paths_defined(self):
        expected = {
            c.DUAL_INVEST_CURRENCY_PAIRS: '/api/v5/dualinvest/currency-pairs',
            c.DUAL_INVEST_PRODUCT_INFO: '/api/v5/dualinvest/product-info',
            c.DUAL_INVEST_REQUEST_QUOTE: '/api/v5/dualinvest/request-quote',
            c.DUAL_INVEST_TRADE: '/api/v5/dualinvest/trade',
            c.DUAL_INVEST_REQUEST_REDEEM_QUOTE: '/api/v5/dualinvest/request-redeem-quote',
            c.DUAL_INVEST_REDEEM: '/api/v5/dualinvest/redeem',
            c.DUAL_INVEST_ORDER_STATE: '/api/v5/dualinvest/order-state',
            c.DUAL_INVEST_ORDER_HISTORY: '/api/v5/dualinvest/order-history',
        }
        for const_value, path in expected.items():
            self.assertEqual(const_value, path)


if __name__ == '__main__':
    unittest.main()
