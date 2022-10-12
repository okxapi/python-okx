
import unittest
from ..okx import BlockTrading
class BlockTradingTest(unittest.TestCase):
    def setUp(self):
        api_key = 'ef06bf27-6a01-4797-b801-e3897031e45d'
        api_secret_key = 'D3620B2660203350EEE80FDF5BE0C960'
        passphrase = 'Beijing123'
        self.BlockTradingAPI = BlockTrading.BlockTradingAPI(use_server_time=False, flag='1')

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


    def test_get_public_trades(self):
        print(self.BlockTradingAPI.get_public_trades())
if __name__ == '__main__':
    unittest.main()