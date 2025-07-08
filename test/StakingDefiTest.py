import unittest
from okx.Finance import StakingDefi


class StakingDefiTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.StackingAPI = StakingDefi.StakingDefiAPI(api_key, api_secret_key, passphrase, use_server_time=False,
                                                      flag='1')

    def test_get_offers(self):
        print(self.StackingAPI.get_offers(ccy="USDT"))

    def test_purcase(self):
        print(self.StackingAPI.purchase(1456,  [{
                "ccy":"USDT",
                "amt":"100"
            }], "100", "0"))

    def test_redeem(self):
        print(self.StackingAPI.redeem(1456,"defi"))

    def test_cancel(self):
        print(self.StackingAPI.cancel(1456,"defi"))

    def test_get_activity_orders(self):
        print(self.StackingAPI.get_activity_orders())

    def test_get_orders_history(self):
        print(self.StackingAPI.get_orders_history())


if __name__ == "__main__":
    unittest.main()
