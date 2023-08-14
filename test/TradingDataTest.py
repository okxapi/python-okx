import unittest
from ..okx import TradingData


class TradingDataTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.TradingDataAPI = TradingData.TradingDataAPI(api_key, api_secret_key, passphrase, use_server_time=False,
                                                         flag='1')
    """
      def test_get_support_coins(self):
        print(self.TradingDataAPI.get_support_coin())
      def test_get_taker_vol(self):
        print(self.TradingDataAPI.get_taker_volume(ccy="BTC",instType="SPOT"))
      def test_get_loan_ratio(self):
        print(self.TradingDataAPI.get_margin_lending_ratio('ETH'))
        def test_get_long_short_account(self):
        print(self.TradingDataAPI.get_long_short_ratio('BTC'))
        def test_get_contracts_vol_open(self):
        print(self.TradingDataAPI.get_contracts_interest_volume(ccy="BTC"))
    def test_get_option_vol_open(self):
        print(self.TradingDataAPI.get_options_interest_volume(ccy="ETH"))
    def test_get_option_ratio(self):
        print(self.TradingDataAPI.get_put_call_ratio(ccy='BTC'))
    def test_get_open_interest_expiry(self):
        print(self.TradingDataAPI.get_interest_volume_expiry("BTC"))
    def test_open_interest_volume_strike(self):
        print(self.TradingDataAPI.get_interest_volume_strike(ccy="BTC",expTime="20220901"))
    
    """
    def test_taker_block_vol(self):
        print(self.TradingDataAPI.get_taker_flow(ccy='BTC'))

if __name__ == "__main__":
    unittest.main()
