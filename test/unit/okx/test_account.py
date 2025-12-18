"""
Unit tests for okx.Account module

Mirrors the structure: okx/Account.py -> test/unit/okx/test_account.py
"""
import unittest
from unittest.mock import patch
from okx.Account import AccountAPI
from okx import consts as c


class TestAccountAPIPositionBuilder(unittest.TestCase):
    """Unit tests for the position_builder method"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = 'test_api_key'
        self.api_secret = 'test_api_secret'
        self.passphrase = 'test_passphrase'
        self.account_api = AccountAPI(
            api_key=self.api_key,
            api_secret_key=self.api_secret,
            passphrase=self.passphrase,
            flag='0'
        )

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_with_all_parameters(self, mock_request):
        """Test position_builder with all parameters provided"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': [{
                'mmr': '1000',
                'imr': '2000',
                'mmrBf': '900',
                'imrBf': '1900'
            }]
        }
        mock_request.return_value = mock_response

        sim_pos = [{'instId': 'BTC-USDT-SWAP', 'pos': '10', 'avgPx': '50000'}]
        sim_asset = [{'ccy': 'USDT', 'amt': '10000'}]

        # Act
        result = self.account_api.position_builder(
            acctLv='2',
            inclRealPosAndEq=True,
            lever='5',
            greeksType='PA',
            simPos=sim_pos,
            simAsset=sim_asset,
            idxVol='0.05'
        )

        # Assert
        expected_params = {
            'acctLv': '2',
            'inclRealPosAndEq': True,
            'lever': '5',
            'greeksType': 'PA',
            'simPos': sim_pos,
            'simAsset': sim_asset,
            'idxVol': '0.05'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_with_idxVol_only(self, mock_request):
        """Test position_builder with only idxVol parameter"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': []
        }
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(idxVol='0.1')

        # Assert
        expected_params = {
            'idxVol': '0.1'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_negative_idxVol(self, mock_request):
        """Test position_builder with negative idxVol (price decrease)"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': []
        }
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(idxVol='-0.05')

        # Assert
        expected_params = {
            'idxVol': '-0.05'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_with_no_parameters(self, mock_request):
        """Test position_builder with no parameters (all None)"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': []
        }
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder()

        # Assert
        # Should pass empty params dict
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, {})
        self.assertEqual(result, mock_response)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_with_simulated_positions(self, mock_request):
        """Test position_builder with simulated positions and assets"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': [{
                'mmr': '5000',
                'imr': '10000'
            }]
        }
        mock_request.return_value = mock_response

        sim_pos = [
            {'instId': 'BTC-USDT-SWAP', 'pos': '10', 'avgPx': '50000'},
            {'instId': 'ETH-USDT-SWAP', 'pos': '100', 'avgPx': '3000'}
        ]
        sim_asset = [
            {'ccy': 'USDT', 'amt': '100000'},
            {'ccy': 'BTC', 'amt': '1'}
        ]

        # Act
        result = self.account_api.position_builder(
            inclRealPosAndEq=False,
            simPos=sim_pos,
            simAsset=sim_asset,
            idxVol='0.1'
        )

        # Assert
        expected_params = {
            'inclRealPosAndEq': False,
            'simPos': sim_pos,
            'simAsset': sim_asset,
            'idxVol': '0.1'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_greeks_type_pa(self, mock_request):
        """Test position_builder with greeksType PA"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(greeksType='PA')

        # Assert
        expected_params = {'greeksType': 'PA'}
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_greeks_type_bs(self, mock_request):
        """Test position_builder with greeksType BS"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(greeksType='BS')

        # Assert
        expected_params = {'greeksType': 'BS'}
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_includes_real_positions(self, mock_request):
        """Test position_builder with inclRealPosAndEq=True"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(
            inclRealPosAndEq=True,
            idxVol='0.05'
        )

        # Assert
        expected_params = {
            'inclRealPosAndEq': True,
            'idxVol': '0.05'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_excludes_real_positions(self, mock_request):
        """Test position_builder with inclRealPosAndEq=False (only virtual positions)"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        sim_pos = [{'instId': 'BTC-USDT-SWAP', 'pos': '5', 'avgPx': '60000'}]

        # Act
        result = self.account_api.position_builder(
            inclRealPosAndEq=False,
            simPos=sim_pos
        )

        # Assert
        expected_params = {
            'inclRealPosAndEq': False,
            'simPos': sim_pos
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_with_account_level(self, mock_request):
        """Test position_builder with specific account level"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(acctLv='3')

        # Assert
        expected_params = {'acctLv': '3'}
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_with_leverage(self, mock_request):
        """Test position_builder with leverage parameter"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(lever='10')

        # Assert
        expected_params = {'lever': '10'}
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_extreme_volatility_positive(self, mock_request):
        """Test position_builder with maximum positive volatility"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(idxVol='1')

        # Assert
        expected_params = {'idxVol': '1'}
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_extreme_volatility_negative(self, mock_request):
        """Test position_builder with maximum negative volatility"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(idxVol='-0.99')

        # Assert
        expected_params = {'idxVol': '-0.99'}
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_position_builder_complex_scenario(self, mock_request):
        """Test position_builder with a complex realistic scenario"""
        # Arrange
        mock_response = {
            'code': '0',
            'msg': '',
            'data': [{
                'mmr': '15000',
                'imr': '30000',
                'mmrBf': '14000',
                'imrBf': '28000',
                'markPxBf': '49500'
            }]
        }
        mock_request.return_value = mock_response

        sim_pos = [
            {'instId': 'BTC-USDT-SWAP', 'pos': '10', 'avgPx': '50000'},
            {'instId': 'ETH-USDT-SWAP', 'pos': '-50', 'avgPx': '3000'}
        ]
        sim_asset = [{'ccy': 'USDT', 'amt': '50000'}]

        # Act - Simulate a 5% market drop
        result = self.account_api.position_builder(
            acctLv='2',
            inclRealPosAndEq=False,
            lever='5',
            greeksType='PA',
            simPos=sim_pos,
            simAsset=sim_asset,
            idxVol='-0.05'
        )

        # Assert
        expected_params = {
            'acctLv': '2',
            'inclRealPosAndEq': False,
            'lever': '5',
            'greeksType': 'PA',
            'simPos': sim_pos,
            'simAsset': sim_asset,
            'idxVol': '-0.05'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)
        self.assertEqual(result['code'], '0')
        self.assertIn('mmrBf', result['data'][0])
        self.assertIn('imrBf', result['data'][0])


class TestAccountAPIPositionBuilderParameterHandling(unittest.TestCase):
    """Test parameter handling and edge cases"""

    def setUp(self):
        """Set up test fixtures"""
        self.account_api = AccountAPI(
            api_key='test_key',
            api_secret_key='test_secret',
            passphrase='test_pass',
            flag='0'
        )

    @patch.object(AccountAPI, '_request_with_params')
    def test_none_parameters_are_excluded(self, mock_request):
        """Test that None parameters are not included in the request"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(
            acctLv='2',
            inclRealPosAndEq=None,  # Should be excluded
            lever=None,  # Should be excluded
            greeksType='PA',
            simPos=None,  # Should be excluded
            simAsset=None,  # Should be excluded
            idxVol='0.05'
        )

        # Assert - Only non-None params should be in the call
        expected_params = {
            'acctLv': '2',
            'greeksType': 'PA',
            'idxVol': '0.05'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_false_value_for_inclRealPosAndEq_is_included(self, mock_request):
        """Test that False value for inclRealPosAndEq is included (not treated as None)"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(inclRealPosAndEq=False)

        # Assert - False should be included
        expected_params = {
            'inclRealPosAndEq': False
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_empty_lists_are_included(self, mock_request):
        """Test that empty lists are included in the request"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(
            simPos=[],
            simAsset=[]
        )

        # Assert
        expected_params = {
            'simPos': [],
            'simAsset': []
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_zero_idxVol_is_included(self, mock_request):
        """Test that zero idxVol is included (represents no volatility change)"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.position_builder(idxVol='0')

        # Assert
        expected_params = {
            'idxVol': '0'
        }
        mock_request.assert_called_once_with(c.POST, c.POSITION_BUILDER, expected_params)


class TestAccountAPISetAutoEarn(unittest.TestCase):
    """Unit tests for the set_auto_earn method"""

    def setUp(self):
        """Set up test fixtures"""
        self.account_api = AccountAPI(
            api_key='test_key',
            api_secret_key='test_secret',
            passphrase='test_pass',
            flag='0'
        )

    @patch.object(AccountAPI, '_request_with_params')
    def test_set_auto_earn_with_all_params(self, mock_request):
        """Test set_auto_earn with all parameters provided"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.set_auto_earn(
            earnType='current',
            ccy='USDT',
            action='start',
            apr='0.05'
        )

        # Assert
        expected_params = {
            'earnType': 'current',
            'ccy': 'USDT',
            'action': 'start',
            'apr': '0.05'
        }
        mock_request.assert_called_once_with(c.POST, c.SET_AUTO_EARN, expected_params)
        self.assertEqual(result, mock_response)

    @patch.object(AccountAPI, '_request_with_params')
    def test_set_auto_earn_start_action(self, mock_request):
        """Test set_auto_earn with start action"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.set_auto_earn(
            earnType='current',
            ccy='BTC',
            action='start'
        )

        # Assert
        expected_params = {
            'earnType': 'current',
            'ccy': 'BTC',
            'action': 'start',
            'apr': ''
        }
        mock_request.assert_called_once_with(c.POST, c.SET_AUTO_EARN, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_set_auto_earn_stop_action(self, mock_request):
        """Test set_auto_earn with stop action"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.set_auto_earn(
            earnType='current',
            ccy='ETH',
            action='stop'
        )

        # Assert
        expected_params = {
            'earnType': 'current',
            'ccy': 'ETH',
            'action': 'stop',
            'apr': ''
        }
        mock_request.assert_called_once_with(c.POST, c.SET_AUTO_EARN, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_set_auto_earn_with_empty_params(self, mock_request):
        """Test set_auto_earn with empty parameters (default values)"""
        # Arrange
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        # Act
        result = self.account_api.set_auto_earn()

        # Assert
        expected_params = {
            'earnType': '',
            'ccy': '',
            'action': '',
            'apr': ''
        }
        mock_request.assert_called_once_with(c.POST, c.SET_AUTO_EARN, expected_params)

    @patch.object(AccountAPI, '_request_with_params')
    def test_set_auto_earn_different_currencies(self, mock_request):
        """Test set_auto_earn with different currencies"""
        mock_response = {'code': '0', 'msg': '', 'data': []}
        mock_request.return_value = mock_response

        currencies = ['USDT', 'BTC', 'ETH', 'USDC']

        for ccy in currencies:
            mock_request.reset_mock()
            result = self.account_api.set_auto_earn(
                earnType='current',
                ccy=ccy,
                action='start'
            )

            call_args = mock_request.call_args[0][2]
            self.assertEqual(call_args['ccy'], ccy)


if __name__ == '__main__':
    unittest.main()

