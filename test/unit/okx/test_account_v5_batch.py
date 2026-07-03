"""
Unit tests for okx.Account v5 API sync batch (0.4.3) — items #2, #6, #8.

Mirrors the existing @patch.object mock pattern in test/unit/okx/test_account.py.
"""
import unittest
from unittest.mock import patch
from okx.Account import AccountAPI
from okx import consts as c

# Placeholder client identifiers — every request is mocked; not real credentials.
_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class _Base(unittest.TestCase):
    def setUp(self):
        self.api = AccountAPI(api_key=_STUB_ID, api_secret_key=_STUB_SIGN, passphrase=_STUB_PHRASE, flag='0')


class TestGetFeeRatesGroupId(_Base):
    """#2 groupId on get_fee_rates"""

    @patch.object(AccountAPI, '_request_with_params')
    def test_backward_compatible_omits_groupId(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_fee_rates('SPOT')
        expected = {'instType': 'SPOT', 'instId': '', 'uly': '', 'category': '', 'instFamily': ''}
        mock_request.assert_called_once_with(c.GET, c.FEE_RATES, expected)

    @patch.object(AccountAPI, '_request_with_params')
    def test_groupId_written_when_set(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_fee_rates('SPOT', groupId='1')
        params = mock_request.call_args[0][2]
        self.assertEqual(params['groupId'], '1')


class TestDeltaNeutralConfig(_Base):
    """#6 set-trading-config + precheck-set-delta-neutral"""

    @patch.object(AccountAPI, '_request_with_params')
    def test_set_trading_config(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.set_trading_config(type='stgyType', stgyType='1')
        mock_request.assert_called_once_with(
            c.POST, c.SET_TRADING_CONFIG, {'type': 'stgyType', 'stgyType': '1'})

    @patch.object(AccountAPI, '_request_with_params')
    def test_set_trading_config_type_only(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.set_trading_config(type='stgyType')
        mock_request.assert_called_once_with(
            c.POST, c.SET_TRADING_CONFIG, {'type': 'stgyType'})

    @patch.object(AccountAPI, '_request_with_params')
    def test_precheck_set_delta_neutral(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.precheck_set_delta_neutral(stgyType='1')
        mock_request.assert_called_once_with(
            c.GET, c.PRECHECK_SET_DELTA_NEUTRAL, {'stgyType': '1'})


class TestBillTypeAndApply(_Base):
    """#8 subtypes + bills-history-archive"""

    @patch.object(AccountAPI, '_request_with_params')
    def test_get_bill_type(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_bill_type()
        mock_request.assert_called_once_with(c.GET, c.BILL_TYPE, {})

    @patch.object(AccountAPI, '_request_with_params')
    def test_get_bill_type_with_type(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_bill_type(type='1')
        mock_request.assert_called_once_with(c.GET, c.BILL_TYPE, {'type': '1'})

    @patch.object(AccountAPI, '_request_with_params')
    def test_apply_bills(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.apply_bills(year='2023', quarter='Q1', type='1')
        mock_request.assert_called_once_with(
            c.POST, c.BILLS_APPLY,
            {'year': '2023', 'quarter': 'Q1', 'type': '1'})

    @patch.object(AccountAPI, '_request_with_params')
    def test_apply_bills_required_only(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.apply_bills(year='2023', quarter='Q1')
        mock_request.assert_called_once_with(
            c.POST, c.BILLS_APPLY, {'year': '2023', 'quarter': 'Q1'})


if __name__ == '__main__':
    unittest.main()
