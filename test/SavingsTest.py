import unittest
from okx.Finance import Savings

class SavingsTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.StackingAPI = Savings.SavingsAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')


    def test_get_saving_balance(self):
        print(self.StackingAPI.get_saving_balance(ccy='USDT'))

    def test_savings_purchase_redemption(self):
        print(self.StackingAPI.savings_purchase_redemption(ccy='USDT',amt="0.1",side="redempt",rate="1"))

    def test_set_lending_rate(self):
        print(self.StackingAPI.set_lending_rate(ccy='USDT',rate="1"))

    def test_get_lending_history(self):
        print(self.StackingAPI.get_lending_history(ccy='USDT'))

    def test_get_public_borrow_history(self):
        print(self.StackingAPI.get_public_borrow_history(ccy='USDT'))

    def test_get_public_borrow_info(self):
        print(self.StackingAPI.get_public_borrow_info(ccy='BTC'))

if __name__ == "__main__":
    unittest.main()