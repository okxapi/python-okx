import unittest
from okx.Finance import SolStaking

class SolStakingTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.StackingAPI = SolStaking.SolStakingAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')

    def test_sol_purchase(self):
        print(self.StackingAPI.sol_purchase(amt="1"))

    def test_sol_redeem(self):
        print(self.StackingAPI.sol_redeem(amt="1"))

    def test_sol_balance(self):
        print(self.StackingAPI.sol_balance())

    def test_sol_purchase_redeem_history(self):
        print(self.StackingAPI.sol_purchase_redeem_history(type="purchase", status="", after="", before="", limit=""))

    def test_sol_apy_history(self):
        print(self.StackingAPI.sol_apy_history(days="7"))

    def test_sol_product_info(self):
        print(self.StackingAPI.sol_product_info())

if __name__ == "__main__":
    unittest.main()