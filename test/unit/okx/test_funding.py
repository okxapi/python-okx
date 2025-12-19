"""
Unit tests for okx.Funding module

Mirrors the structure: okx/Funding.py -> test/unit/okx/test_funding.py
"""
import unittest
from unittest.mock import patch
from okx.Funding import FundingAPI
from okx import consts as c


class TestFundingAPIWithdrawal(unittest.TestCase):
    """Unit tests for the withdrawal method"""

    def setUp(self):
        """Set up test fixtures"""
        self.funding_api = FundingAPI(
            api_key='test_key',
            api_secret_key='test_secret',
            passphrase='test_pass',
            flag='0'
        )

    @patch.object(FundingAPI, '_request_with_params')
    def test_withdrawal_with_required_params(self, mock_request):
        """Test withdrawal with required parameters only"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': [{'wdId': '12345'}]}
        mock_request.return_value = mock_response

        # Act
        result = self.funding_api.withdrawal(
            ccy='USDT',
            amt='100',
            dest='4',
            toAddr='0x1234567890abcdef'
        )

        # Assert
        expected_params = {
            'ccy': 'USDT',
            'amt': '100',
            'dest': '4',
            'toAddr': '0x1234567890abcdef',
            'chain': '',
            'areaCode': '',
            'clientId': ''
        }
        mock_request.assert_called_once_with(c.POST, c.WITHDRAWAL_COIN, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(FundingAPI, '_request_with_params')
    def test_withdrawal_with_all_params(self, mock_request):
        """Test withdrawal with all parameters provided"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': [{'wdId': '12345'}]}
        mock_request.return_value = mock_response

        # Act
        result = self.funding_api.withdrawal(
            ccy='USDT',
            amt='100',
            dest='4',
            toAddr='0x1234567890abcdef',
            chain='USDT-TRC20',
            areaCode='86',
            clientId='client123',
            toAddrType='1'
        )

        # Assert
        expected_params = {
            'ccy': 'USDT',
            'amt': '100',
            'dest': '4',
            'toAddr': '0x1234567890abcdef',
            'chain': 'USDT-TRC20',
            'areaCode': '86',
            'clientId': 'client123',
            'toAddrType': '1'
        }
        mock_request.assert_called_once_with(c.POST, c.WITHDRAWAL_COIN, expected_params)

    @patch.object(FundingAPI, '_request_with_params')
    def test_withdrawal_with_toAddrType_okx_account(self, mock_request):
        """Test withdrawal with toAddrType for OKX account"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.funding_api.withdrawal(
            ccy='USDT',
            amt='50',
            dest='3',
            toAddr='user@example.com',
            toAddrType='1'  # OKX account
        )

        # Assert
        call_args = mock_request.call_args[0][2]
        self.assertEqual(call_args['toAddrType'], '1')

    @patch.object(FundingAPI, '_request_with_params')
    def test_withdrawal_with_toAddrType_external(self, mock_request):
        """Test withdrawal with toAddrType for external address"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.funding_api.withdrawal(
            ccy='BTC',
            amt='0.1',
            dest='4',
            toAddr='bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
            toAddrType='2'  # External address
        )

        # Assert
        call_args = mock_request.call_args[0][2]
        self.assertEqual(call_args['toAddrType'], '2')


class TestFundingAPIGetWithdrawalHistory(unittest.TestCase):
    """Unit tests for the get_withdrawal_history method"""

    def setUp(self):
        """Set up test fixtures"""
        self.funding_api = FundingAPI(
            api_key='test_key',
            api_secret_key='test_secret',
            passphrase='test_pass',
            flag='0'
        )

    @patch.object(FundingAPI, '_request_with_params')
    def test_get_withdrawal_history_with_no_params(self, mock_request):
        """Test get_withdrawal_history with no parameters"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.funding_api.get_withdrawal_history()

        # Assert
        call_args = mock_request.call_args[0][2]
        self.assertNotIn('toAddrType', call_args)
        self.assertEqual(result, mock_response)

    @patch.object(FundingAPI, '_request_with_params')
    def test_get_withdrawal_history_with_toAddrType(self, mock_request):
        """Test get_withdrawal_history with toAddrType parameter"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.funding_api.get_withdrawal_history(
            ccy='USDT',
            toAddrType='1'
        )

        # Assert
        call_args = mock_request.call_args[0][2]
        self.assertEqual(call_args['ccy'], 'USDT')
        self.assertEqual(call_args['toAddrType'], '1')

    @patch.object(FundingAPI, '_request_with_params')
    def test_get_withdrawal_history_with_all_params(self, mock_request):
        """Test get_withdrawal_history with all parameters"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.funding_api.get_withdrawal_history(
            ccy='BTC',
            wdId='12345',
            clientId='client123',
            txId='tx123',
            type='1',
            state='2',
            after='1609459200000',
            before='1609545600000',
            limit='10',
            toAddrType='2'
        )

        # Assert
        expected_params = {
            'ccy': 'BTC',
            'wdId': '12345',
            'clientId': 'client123',
            'txId': 'tx123',
            'type': '1',
            'state': '2',
            'after': '1609459200000',
            'before': '1609545600000',
            'limit': '10',
            'toAddrType': '2'
        }
        mock_request.assert_called_once_with(c.GET, c.GET_WITHDRAWAL_HISTORY, expected_params)

    @patch.object(FundingAPI, '_request_with_params')
    def test_get_withdrawal_history_filter_by_state(self, mock_request):
        """Test get_withdrawal_history filtering by state"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        states = ['0', '1', '2', '3', '4', '5']

        for state in states:
            mock_request.reset_mock()
            result = self.funding_api.get_withdrawal_history(state=state)

            call_args = mock_request.call_args[0][2]
            self.assertEqual(call_args['state'], state)


if __name__ == '__main__':
    unittest.main()

