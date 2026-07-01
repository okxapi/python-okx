"""
Unit tests for okx.Finance.Earn EarnAPI — item #9.
"""
import unittest
from unittest.mock import patch
from okx.Finance.Earn import EarnAPI
from okx import consts as c

# Placeholder client identifiers — every request is mocked; not real credentials.
_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestEarnAPI(unittest.TestCase):
    def setUp(self):
        self.api = EarnAPI(api_key=_STUB_ID, api_secret_key=_STUB_SIGN, passphrase=_STUB_PHRASE, flag='0')

    @patch.object(EarnAPI, '_request_with_params')
    def test_staking_cancel_redeem(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.staking_cancel_redeem(ordId='754147')
        mock_request.assert_called_once_with(c.POST, c.STAKING_CANCEL_REDEEM, {'ordId': '754147'})

    @patch.object(EarnAPI, '_request_with_params')
    def test_get_staking_products_default_empty(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_staking_products()
        mock_request.assert_called_once_with(c.GET, c.STAKING_PRODUCTS, {})

    @patch.object(EarnAPI, '_request_with_params')
    def test_get_staking_products_with_filters(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_staking_products(ccy='ETH', productId='p1')
        mock_request.assert_called_once_with(
            c.GET, c.STAKING_PRODUCTS, {'ccy': 'ETH', 'productId': 'p1'})


if __name__ == '__main__':
    unittest.main()
