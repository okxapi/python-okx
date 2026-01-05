import unittest
from okx import TradingData
from test.config import get_api_credentials


class TradingDataTest(unittest.TestCase):
    def setUp(self):
        api_key, api_secret_key, passphrase, flag = get_api_credentials()
        self.TradingDataAPI = TradingData.TradingDataAPI(api_key, api_secret_key, passphrase, use_server_time=False,
                                                         flag=flag)
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

    def test_get_contracts_open_interest_history(self):
        print(self.TradingDataAPI.get_contracts_open_interest_history(instId='BTC-USDT-SWAP'))

    def test_get_contracts_open_interest_history_with_params(self):
        print(self.TradingDataAPI.get_contracts_open_interest_history(
            instId='BTC-USDT-SWAP',
            period='1H',
            limit='50'
        ))

if __name__ == "__main__":
    unittest.main()
