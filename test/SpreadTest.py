import unittest
from okx import SpreadTrading
class TradeTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.tradeApi = SpreadTrading.SpreadTradingAPI(api_key, api_secret_key, passphrase, False, '1')

    # def test_place_order(self):
    #     print(self.tradeApi.place_order(sprdId='BTC-USDT_BTC-USDT-SWAP',clOrdId='b15',side='buy',ordType='limit',
    #                                     px='2',sz='2'))
    #{'code': '0', 'msg': '', 'data': [{'ordId': '1899422086260064256', 'clOrdId': 'b15', 'tag': '', 'sCode': '0', 'sMsg': ''}]}

    # def test_cancel_order(self):
    #     print(self.tradeApi.cancel_order(ordId='1899422086260064256'))

    # def test_cancel_all_orders(self):
    #     print(self.tradeApi.cancel_all_orders(sprdId='BTC-USDT_BTC-USDT-SWAP'))


    #{'code': '0', 'msg': '','data': [{'ordId': '1899453539647750144', 'clOrdId': 'b15', 'tag': '', 'sCode': '0',
    # 'sMsg': ''}]}
    # def test_get_order_details(self):
    #     print(self.tradeApi.get_order_details(ordId='1899453539647750144'))

    # def test_get_active_orders(self):
    #     print(self.tradeApi.get_active_orders())

    # def test_get_orders(self):
    #     print(self.tradeApi.get_orders())

    # def test_get_spreads(self):
    #     print(self.tradeApi.get_spreads())

    # def test_get_order_book(self):
    #     print(self.tradeApi.get_order_book(sprdId='ETH-USDT-SWAP_ETH-USDT-230929'))
    #
    # def test_get_ticker(self):
    #     print(self.tradeApi.get_ticker(sprdId='ETH-USDT-SWAP_ETH-USDT-230929'))
    #
    def test_get_public_trades(self):
        print(self.tradeApi.get_public_trades(sprdId='ETH-USDT-SWAP_ETH-USDT-230929'))

if __name__=='__main__':
    unittest.main()
