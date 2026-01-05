"""
Unit tests for okx.TradingData module

Mirrors the structure: okx/TradingData.py -> test/unit/okx/test_trading_data.py
"""
import unittest
from unittest.mock import patch
from okx.TradingData import TradingDataAPI
from okx import consts as c


class TestTradingDataAPIContractsOpenInterestHistory(unittest.TestCase):
    """Unit tests for the get_contracts_open_interest_history method"""

    def setUp(self):
        """Set up test fixtures"""
        self.trading_data_api = TradingDataAPI(flag='0')

    @patch.object(TradingDataAPI, '_request_with_params')
    def test_get_contracts_open_interest_history_with_required_params(self, mock_request):
        """Test get_contracts_open_interest_history with required parameters only"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': [
                {'ts': '1609459200000', 'oi': '100000', 'oiCcy': '10'}
            ]
        }
        mock_request.return_value = mock_response

        # Act
        result = self.trading_data_api.get_contracts_open_interest_history(
            instId='BTC-USDT-SWAP'
        )

        # Assert
        expected_params = {
            'instId': 'BTC-USDT-SWAP'
        }
        mock_request.assert_called_once_with(c.GET, c.CONTRACTS_OPEN_INTEREST_HISTORY, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(TradingDataAPI, '_request_with_params')
    def test_get_contracts_open_interest_history_with_all_params(self, mock_request):
        """Test get_contracts_open_interest_history with all parameters provided"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': [
                {'ts': '1609459200000', 'oi': '100000', 'oiCcy': '10'}
            ]
        }
        mock_request.return_value = mock_response

        # Act
        result = self.trading_data_api.get_contracts_open_interest_history(
            instId='BTC-USDT-SWAP',
            period='1H',
            begin='1609459200000',
            end='1609545600000',
            limit='50'
        )

        # Assert
        expected_params = {
            'instId': 'BTC-USDT-SWAP',
            'period': '1H',
            'begin': '1609459200000',
            'end': '1609545600000',
            'limit': '50'
        }
        mock_request.assert_called_once_with(c.GET, c.CONTRACTS_OPEN_INTEREST_HISTORY, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(TradingDataAPI, '_request_with_params')
    def test_get_contracts_open_interest_history_with_period(self, mock_request):
        """Test get_contracts_open_interest_history with period parameter"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.trading_data_api.get_contracts_open_interest_history(
            instId='ETH-USDT-SWAP',
            period='5m'
        )

        # Assert
        expected_params = {
            'instId': 'ETH-USDT-SWAP',
            'period': '5m'
        }
        mock_request.assert_called_once_with(c.GET, c.CONTRACTS_OPEN_INTEREST_HISTORY, expected_params)

    @patch.object(TradingDataAPI, '_request_with_params')
    def test_get_contracts_open_interest_history_different_periods(self, mock_request):
        """Test get_contracts_open_interest_history with different period values"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        periods = ['5m', '15m', '30m', '1H', '2H', '4H', '6H', '12H', '1D', '2D', '3D', '5D', '1W', '1M', '3M']
        
        for period in periods:
            mock_request.reset_mock()
            result = self.trading_data_api.get_contracts_open_interest_history(
                instId='BTC-USDT-SWAP',
                period=period
            )
            
            call_args = mock_request.call_args[0][2]
            self.assertEqual(call_args['period'], period)

    @patch.object(TradingDataAPI, '_request_with_params')
    def test_get_contracts_open_interest_history_different_inst_ids(self, mock_request):
        """Test get_contracts_open_interest_history with different instrument IDs"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        inst_ids = ['BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'BTC-USD-SWAP', 'BTC-USDT-240329']
        
        for inst_id in inst_ids:
            mock_request.reset_mock()
            result = self.trading_data_api.get_contracts_open_interest_history(
                instId=inst_id
            )
            
            call_args = mock_request.call_args[0][2]
            self.assertEqual(call_args['instId'], inst_id)

    @patch.object(TradingDataAPI, '_request_with_params')
    def test_get_contracts_open_interest_history_with_pagination(self, mock_request):
        """Test get_contracts_open_interest_history with pagination parameters"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.trading_data_api.get_contracts_open_interest_history(
            instId='BTC-USDT-SWAP',
            begin='1609459200000',
            end='1609545600000',
            limit='100'
        )

        # Assert
        expected_params = {
            'instId': 'BTC-USDT-SWAP',
            'begin': '1609459200000',
            'end': '1609545600000',
            'limit': '100'
        }
        mock_request.assert_called_once_with(c.GET, c.CONTRACTS_OPEN_INTEREST_HISTORY, expected_params)

    @patch.object(TradingDataAPI, '_request_with_params')
    def test_get_contracts_open_interest_history_utc_periods(self, mock_request):
        """Test get_contracts_open_interest_history with UTC+0 period values"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        utc_periods = ['6Hutc', '12Hutc', '1Dutc', '2Dutc', '3Dutc', '5Dutc', '1Wutc', '1Mutc', '3Mutc']
        
        for period in utc_periods:
            mock_request.reset_mock()
            result = self.trading_data_api.get_contracts_open_interest_history(
                instId='BTC-USDT-SWAP',
                period=period
            )
            
            call_args = mock_request.call_args[0][2]
            self.assertEqual(call_args['period'], period)


if __name__ == '__main__':
    unittest.main()

