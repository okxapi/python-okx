
import unittest
from okx import BlockTrading
class BlockTradingTest(unittest.TestCase):
    def setUp(self):
        api_key = 'a6f1e378-1c03-472d-ada0-710f4d51eebf'
        api_secret_key = '74A6E1E03700D5EFCC2BBB7782170189'
        passphrase = 'Qa131415!'
        self.BlockTradingAPI = BlockTrading.BlockTradingAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')

    """
    def test_get_counter_parties(self):
        print(self.BlockTradingAPI.counterparties())
    def test_create_rfqs(self):
        counterparties=['HWZ']
        legs =[{
            'instId':"BTC-USDT",
            'sz':'25',
            'side':'buy'
        }]
        print(self.BlockTradingAPI.create_rfq(counterparties,legs = legs))
    def test_cancel_rfq(self):###'rfqId': '3I1MK3O'
        print(self.BlockTradingAPI.cancel_rfq(rfqId='3I1MK3O'))
    def test_cancel_batch_rfqs(self):
        #3I1MK40
        #3I1MK48
        print(self.BlockTradingAPI.cancel_batch_rfqs(["3I1MK40","3I1MK48"]))
    def test_cancel_all_rfqs(self):
        print(self.BlockTradingAPI.cancel_all_rfqs())
    def test_execute_quotes(self):
        print(self.BlockTradingAPI.execute_quote("3I1MJE0","AC1233"))
    def test_create_quotes(self):
        print(self.BlockTradingAPI.create_quote("3I1MJE0",))
    def test_get_rfqs(self):
        print(self.BlockTradingAPI.get_rfqs())
    def test_get_quotes(self):
        print(self.BlockTradingAPI.get_quotes())
    def test_get_public_trades(self):
        print(self.BlockTradingAPI.get_public_trades())
    def test_get_trade(self):
        print(self.BlockTradingAPI.get_trades())
    """


    # def test_get_public_trades(self):
    #     print(self.BlockTradingAPI.get_public_trades())

    # def test_get_quote_products(self):
    #     print(self.BlockTradingAPI.get_quote_products())

    def test_create_rfqs(self):
        counterparties=['8924']
        legs =[{
            'instId':"BTC-USDT",
            'sz':'25',
            'side':'buy',
            'posSide':'net',
            'tdMode':'cross',
            'ccy':'USDT'
        }]
        print(self.BlockTradingAPI.create_rfq(counterparties,allowPartialExecution='true',tag='1234',legs = legs))

    # def test_execute_quotes(self):
    #     legs = [{
    #                 'instId':"BTC-USDT",
    #                 'sz':'0.0001',
    #             }]
    #     print(self.BlockTradingAPI.execute_quote("3IR9E68","3IR9E80",legs))

    # def test_create_quotes(self):
    #     legs = [{
    #         'instId': "BTC-USDT",
    #         'sz': '25',
    #         'side': 'buy',
    #         'posSide': 'net',
    #         'tdMode': 'cross',
    #         'ccy': 'USDT'
    #     }]
    #     print(self.BlockTradingAPI.create_quote(rfqId='3IR9BT8',quoteSide='buy',legs=legs))

    # def test_get_trade(self):
    #     print(self.BlockTradingAPI.get_trades())



if __name__ == '__main__':
    unittest.main()