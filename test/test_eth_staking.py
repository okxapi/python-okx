import unittest
from okx.Finance import EthStaking
from test.config import get_api_credentials


class EthStakingTest(unittest.TestCase):
    def setUp(self):
        api_key, api_secret_key, passphrase, flag = get_api_credentials()
        self.StackingAPI = EthStaking.EthStakingAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag=flag)

    def test_eth_product_info(self):
        print(self.StackingAPI.eth_product_info())

    def test_eth_purchase(self):
        print(self.StackingAPI.eth_purchase(amt="1"))

    def test_eth_redeem(self):
        print(self.StackingAPI.eth_redeem(amt="1"))

    def test_eth_balance(self):
        print(self.StackingAPI.eth_balance())

    def test_eth_purchase_redeem_history(self):
        print(self.StackingAPI.eth_purchase_redeem_history(type="", status="", after="", before="", limit=""))

    def test_eth_apy_history(self):
        print(self.StackingAPI.eth_apy_history(days="7"))

if __name__ == "__main__":
    unittest.main()