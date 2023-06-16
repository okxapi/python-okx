import unittest
from okx import CopyTrading

class CopyTradingTest(unittest.TestCase):
    def setUp(self):
        api_key = 'd4ee8839-1142-41c0-add5-e2e82a91efd2'
        api_secret_key = '57E5BEFAB7BD024A91647819E9BCA285'
        passphrase = '123456aA.'
        self.StackingAPI = CopyTrading.CopyTradingAPI(api_key, api_secret_key, passphrase, use_server_time=False,
                                                      flag='0')

    # def test_get_existing_leading_positions(self):
    #     print(self.StackingAPI.get_existing_leading_positions(instId='DOGE-USDT-SWAP'))

    # def test_get_leading_position_history(self):
    #     print(self.StackingAPI.get_leading_position_history())

    # def test_place_leading_stop_order(self):
    #     print(self.StackingAPI.place_leading_stop_order(subPosId='581247467976732672',tpTriggerPx='1'))
    #
    # def test_close_leading_position(self):
    #     print(self.StackingAPI.close_leading_position(subPosId='581247467976732672'))

    # def test_get_leading_instruments(self):
    #     print(self.StackingAPI.get_leading_instruments())

    # def test_amend_leading_instruments(self):
    #     print(self.StackingAPI.amend_leading_instruments(instId='AAVE-USDT-SWAP'))
    #
    # def test_get_profit_sharing_details(self):
    #     print(self.StackingAPI.get_profit_sharing_details())
    #
    # def test_get_total_profit_sharing(self):
    #     print(self.StackingAPI.get_total_profit_sharing())
    #
    def test_get_unrealized_profit_sharing_details(self):
        print(self.StackingAPI.get_unrealized_profit_sharing_details())

if __name__ == "__main__":
    unittest.main()