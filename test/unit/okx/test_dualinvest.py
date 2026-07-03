"""
Unit tests for okx.DualInvest DualInvestAPI — item #10 (8 endpoints, /api/v5/finance/sfp/dcd/*).
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


class TestDualInvestParamMethods(_Base):
    @patch.object(DualInvestAPI, '_request_with_params')
    def test_get_product_info(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_product_info(baseCcy='BTC', quoteCcy='USDT', optType='call')
        mock_request.assert_called_once_with(
            c.GET, c.DUAL_INVEST_PRODUCT_INFO,
            {'baseCcy': 'BTC', 'quoteCcy': 'USDT', 'optType': 'call'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_request_quote(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.request_quote(productId='p1', notionalSz='100', notionalCcy='USDT')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_REQUEST_QUOTE,
            {'productId': 'p1', 'notionalSz': '100', 'notionalCcy': 'USDT'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_trade(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.trade(quoteId='q1')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_TRADE, {'quoteId': 'q1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_request_redeem_quote(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.request_redeem_quote(ordId='o1')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_REQUEST_REDEEM_QUOTE, {'ordId': 'o1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_redeem(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.redeem(ordId='o1', quoteId='q1')
        mock_request.assert_called_once_with(
            c.POST, c.DUAL_INVEST_REDEEM, {'ordId': 'o1', 'quoteId': 'q1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_get_order_state(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_order_state(ordId='o1')
        mock_request.assert_called_once_with(c.GET, c.DUAL_INVEST_ORDER_STATE, {'ordId': 'o1'})

    @patch.object(DualInvestAPI, '_request_with_params')
    def test_get_order_history(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_order_history(ordId='o1', productId='p1', state='filled', limit='10')
        mock_request.assert_called_once_with(
            c.GET, c.DUAL_INVEST_ORDER_HISTORY,
            {'ordId': 'o1', 'productId': 'p1', 'uly': '', 'state': 'filled',
             'beginId': '', 'endId': '', 'begin': '', 'end': '', 'limit': '10'})


class TestDualInvestConstants(unittest.TestCase):
    def test_all_eight_paths_defined(self):
        expected = {
            c.DUAL_INVEST_CURRENCY_PAIRS: '/api/v5/finance/sfp/dcd/currency-pair',
            c.DUAL_INVEST_PRODUCT_INFO: '/api/v5/finance/sfp/dcd/products',
            c.DUAL_INVEST_REQUEST_QUOTE: '/api/v5/finance/sfp/dcd/quote',
            c.DUAL_INVEST_TRADE: '/api/v5/finance/sfp/dcd/trade',
            c.DUAL_INVEST_REQUEST_REDEEM_QUOTE: '/api/v5/finance/sfp/dcd/redeem-quote',
            c.DUAL_INVEST_REDEEM: '/api/v5/finance/sfp/dcd/redeem',
            c.DUAL_INVEST_ORDER_STATE: '/api/v5/finance/sfp/dcd/order-status',
            c.DUAL_INVEST_ORDER_HISTORY: '/api/v5/finance/sfp/dcd/order-history',
        }
        for const_value, path in expected.items():
            self.assertEqual(const_value, path)


if __name__ == '__main__':
    unittest.main()
