"""
Unit tests for okx.Finance.Okusd OkusdAPI — TD 0.4.4 items #7-11
(GET okusd/account, rate/history, subscribe/history, redeem/history, rewards/history).
"""
import unittest
from unittest.mock import patch
from okx.Finance.Okusd import OkusdAPI
from okx import consts as c

_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestOkusdAPI(unittest.TestCase):
    def setUp(self):
        self.api = OkusdAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0',
        )

    def test_constant_paths(self):
        self.assertEqual(c.OKUSD_ACCOUNT, '/api/v5/finance/okusd/account')
        self.assertEqual(c.OKUSD_RATE_HISTORY, '/api/v5/finance/okusd/rate/history')
        self.assertEqual(c.OKUSD_SUBSCRIBE_HISTORY, '/api/v5/finance/okusd/subscribe/history')
        self.assertEqual(c.OKUSD_REDEEM_HISTORY, '/api/v5/finance/okusd/redeem/history')
        self.assertEqual(c.OKUSD_REWARDS_HISTORY, '/api/v5/finance/okusd/rewards/history')

    @patch.object(OkusdAPI, '_request_without_params')
    def test_get_account(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_account()
        mock_request.assert_called_once_with(c.GET, c.OKUSD_ACCOUNT)

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_rate_history_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_rate_history()
        mock_request.assert_called_once_with(c.GET, c.OKUSD_RATE_HISTORY, {})

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_rate_history_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_rate_history(limit='50', begin='1', end='2')
        mock_request.assert_called_once_with(
            c.GET, c.OKUSD_RATE_HISTORY, {'limit': '50', 'begin': '1', 'end': '2'})

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_subscribe_history_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_subscribe_history()
        mock_request.assert_called_once_with(c.GET, c.OKUSD_SUBSCRIBE_HISTORY, {})

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_subscribe_history_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_subscribe_history(limit='100', begin='1', end='2')
        mock_request.assert_called_once_with(
            c.GET, c.OKUSD_SUBSCRIBE_HISTORY, {'limit': '100', 'begin': '1', 'end': '2'})

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_redeem_history_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_redeem_history()
        mock_request.assert_called_once_with(c.GET, c.OKUSD_REDEEM_HISTORY, {})

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_redeem_history_with_type(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_redeem_history(limit='100', begin='1', end='2', type='fast')
        mock_request.assert_called_once_with(
            c.GET, c.OKUSD_REDEEM_HISTORY,
            {'limit': '100', 'begin': '1', 'end': '2', 'type': 'fast'})

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_rewards_history_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_rewards_history()
        mock_request.assert_called_once_with(c.GET, c.OKUSD_REWARDS_HISTORY, {})

    @patch.object(OkusdAPI, '_request_with_params')
    def test_get_rewards_history_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_rewards_history(limit='30', begin='1', end='2')
        mock_request.assert_called_once_with(
            c.GET, c.OKUSD_REWARDS_HISTORY, {'limit': '30', 'begin': '1', 'end': '2'})


if __name__ == '__main__':
    unittest.main()
