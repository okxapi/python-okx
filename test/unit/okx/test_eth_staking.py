"""
Unit tests for okx.Finance.EthStaking EthStakingAPI.eth_cancel_redeem — TD 239 item #2
(POST /api/v5/finance/staking-defi/eth/cancel-redeem). Mirrors eth_purchase / eth_redeem.
"""
import unittest
from unittest.mock import patch
from okx.Finance.EthStaking import EthStakingAPI
from okx import consts as c

# Placeholder client identifiers for constructing the API client in unit tests.
# Every request is mocked (see @patch.object below), so these dummy strings are
# never signed or transmitted — they are not real credentials.
_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestEthCancelRedeem(unittest.TestCase):
    def setUp(self):
        self.api = EthStakingAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0',
        )

    def test_cancel_redeem_constant_path(self):
        # constant targets the official cancel-redeem endpoint
        self.assertEqual(
            c.STACK_ETH_CANCEL_REDEEM,
            '/api/v5/finance/staking-defi/eth/cancel-redeem',
        )

    @patch.object(EthStakingAPI, '_request_with_params')
    def test_eth_cancel_redeem_builds_request(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.eth_cancel_redeem(ordId='1234567890')
        mock_request.assert_called_once_with(
            c.POST, c.STACK_ETH_CANCEL_REDEEM, {'ordId': '1234567890'})

    @patch.object(EthStakingAPI, '_request_with_params')
    def test_eth_cancel_redeem_default_ordid(self, mock_request):
        # additive/back-compat: ordId defaults to '' like eth_purchase/eth_redeem
        mock_request.return_value = {'code': '0'}
        self.api.eth_cancel_redeem()
        mock_request.assert_called_once_with(
            c.POST, c.STACK_ETH_CANCEL_REDEEM, {'ordId': ''})


if __name__ == "__main__":
    unittest.main()
