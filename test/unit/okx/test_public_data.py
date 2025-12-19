"""
Unit tests for okx.PublicData module

Mirrors the structure: okx/PublicData.py -> test/unit/okx/test_public_data.py
"""
import unittest
from unittest.mock import patch
from okx.PublicData import PublicAPI
from okx import consts as c


class TestPublicAPIMarketDataHistory(unittest.TestCase):
    """Unit tests for the get_market_data_history method"""

    def setUp(self):
        """Set up test fixtures"""
        self.public_api = PublicAPI(flag='0')

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_market_data_history_with_required_params(self, mock_request):
        """Test get_market_data_history with required parameters only"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': [{'ts': '1234567890', 'vol': '1000'}]
        }
        mock_request.return_value = mock_response

        # Act
        result = self.public_api.get_market_data_history(
            module='volume',
            instType='SPOT',
            dateAggrType='1D',
            begin='1609459200000',
            end='1609545600000'
        )

        # Assert
        expected_params = {
            'module': 'volume',
            'instType': 'SPOT',
            'dateAggrType': '1D',
            'begin': '1609459200000',
            'end': '1609545600000'
        }
        mock_request.assert_called_once_with(c.GET, c.MARKET_DATA_HISTORY, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_market_data_history_with_all_params(self, mock_request):
        """Test get_market_data_history with all parameters provided"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': [{'ts': '1234567890', 'vol': '1000'}]
        }
        mock_request.return_value = mock_response

        # Act
        result = self.public_api.get_market_data_history(
            module='volume',
            instType='SWAP',
            dateAggrType='1W',
            begin='1609459200000',
            end='1609545600000',
            instIdList='BTC-USDT-SWAP,ETH-USDT-SWAP',
            instFamilyList='BTC-USDT,ETH-USDT'
        )

        # Assert
        expected_params = {
            'module': 'volume',
            'instType': 'SWAP',
            'dateAggrType': '1W',
            'begin': '1609459200000',
            'end': '1609545600000',
            'instIdList': 'BTC-USDT-SWAP,ETH-USDT-SWAP',
            'instFamilyList': 'BTC-USDT,ETH-USDT'
        }
        mock_request.assert_called_once_with(c.GET, c.MARKET_DATA_HISTORY, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_market_data_history_with_inst_id_list(self, mock_request):
        """Test get_market_data_history with instIdList parameter"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.public_api.get_market_data_history(
            module='volume',
            instType='SPOT',
            dateAggrType='1D',
            begin='1609459200000',
            end='1609545600000',
            instIdList='BTC-USDT'
        )

        # Assert
        expected_params = {
            'module': 'volume',
            'instType': 'SPOT',
            'dateAggrType': '1D',
            'begin': '1609459200000',
            'end': '1609545600000',
            'instIdList': 'BTC-USDT'
        }
        mock_request.assert_called_once_with(c.GET, c.MARKET_DATA_HISTORY, expected_params)

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_market_data_history_with_inst_family_list(self, mock_request):
        """Test get_market_data_history with instFamilyList parameter"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.public_api.get_market_data_history(
            module='openInterest',
            instType='FUTURES',
            dateAggrType='1M',
            begin='1609459200000',
            end='1612137600000',
            instFamilyList='BTC-USD'
        )

        # Assert
        expected_params = {
            'module': 'openInterest',
            'instType': 'FUTURES',
            'dateAggrType': '1M',
            'begin': '1609459200000',
            'end': '1612137600000',
            'instFamilyList': 'BTC-USD'
        }
        mock_request.assert_called_once_with(c.GET, c.MARKET_DATA_HISTORY, expected_params)

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_market_data_history_different_inst_types(self, mock_request):
        """Test get_market_data_history with different instType values"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        inst_types = ['SPOT', 'SWAP', 'FUTURES', 'OPTION']
        
        for inst_type in inst_types:
            mock_request.reset_mock()
            result = self.public_api.get_market_data_history(
                module='volume',
                instType=inst_type,
                dateAggrType='1D',
                begin='1609459200000',
                end='1609545600000'
            )
            
            call_args = mock_request.call_args
            self.assertEqual(call_args[0][1], c.MARKET_DATA_HISTORY)
            self.assertEqual(call_args[1]['instType'] if call_args[1] else call_args[0][2]['instType'], inst_type)

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_market_data_history_different_date_aggr_types(self, mock_request):
        """Test get_market_data_history with different dateAggrType values"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        date_aggr_types = ['1D', '1W', '1M']
        
        for aggr_type in date_aggr_types:
            mock_request.reset_mock()
            result = self.public_api.get_market_data_history(
                module='volume',
                instType='SPOT',
                dateAggrType=aggr_type,
                begin='1609459200000',
                end='1609545600000'
            )
            
            call_args = mock_request.call_args[0][2]
            self.assertEqual(call_args['dateAggrType'], aggr_type)

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_market_data_history_different_modules(self, mock_request):
        """Test get_market_data_history with different module values"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        modules = ['volume', 'openInterest', 'tradeCount']
        
        for module in modules:
            mock_request.reset_mock()
            result = self.public_api.get_market_data_history(
                module=module,
                instType='SPOT',
                dateAggrType='1D',
                begin='1609459200000',
                end='1609545600000'
            )
            
            call_args = mock_request.call_args[0][2]
            self.assertEqual(call_args['module'], module)


if __name__ == '__main__':
    unittest.main()

