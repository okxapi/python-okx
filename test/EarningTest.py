import unittest
from okx import Earning

class EarningTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.StackingAPI = Earning.EarningAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='0')

    def test_get_saving_balance(self):
        print(self.StackingAPI.get_saving_balance(ccy='USDT'))

    # def test_savings_purchase_redemption(self):
    #     print(self.StackingAPI.savings_purchase_redemption(ccy='USDT',amt="0.1",side="redempt",rate="1"))

    # def test_set_lending_rate(self):
    #     print(self.StackingAPI.set_lending_rate(ccy='USDT',rate="1"))

    # def test_get_lending_history(self):
    #     print(self.StackingAPI.get_lending_history(ccy='USDT'))

    # def test_get_public_borrow_info(self):
    #     print(self.StackingAPI.get_public_borrow_info(ccy='USDT'))

    # def test_get_public_borrow_history(self):
    #     print(self.StackingAPI.get_public_borrow_history(ccy='USDT'))

    # def setUp(self):
    #     api_key = 'da097c9c-2f77-4dea-be18-2bfa77d0e394'
    #     api_secret_key = '56CC6C72D6B8A46EC993D48C83142A25'
    #     passphrase = '123456aA.'
    #     self.StackingAPI = Earning.EarningAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')
    
    # def test_purcase(self):
    #     investData = [{
    #         'ccy': 'USDT',
    #         'amt': '50'
    #     }]
    #     print(self.StackingAPI.purchase(productId='1456', investData=investData,term='100',tag='dfg'))

    # def test_eth_product_info(self):
    #     print(self.StackingAPI.eth_product_info())

    # def test_eth_purchase(self):
    #     print(self.StackingAPI.eth_purchase(amt="1"))

    # def test_eth_redeem(self):
    #     print(self.StackingAPI.eth_redeem(amt="1"))

    # def test_eth_balance(self):
    #     print(self.StackingAPI.eth_balance())

    # def test_eth_purchase_redeem_history(self):
    #     print(self.StackingAPI.eth_purchase_redeem_history(type="purchase", status="", after="", before="", limit=""))

    # def test_eth_apy_history(self):
    #     print(self.StackingAPI.eth_apy_history(days="7"))

if __name__ == "__main__":
    unittest.main()