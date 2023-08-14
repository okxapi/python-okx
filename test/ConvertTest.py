import unittest
from ..okx import Convert
class ConvertTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.ConvertAPI = Convert.ConvertAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')
    '''
    
    def test_get_currencies(self):
        print(self.ConvertAPI.get_currencies())
    def test_get_currency_pair(self):
        print(self.ConvertAPI.get_currency_pair("USDT","BTC"))
    def test_query_estimate(self):
        print(self.ConvertAPI.estimate_quote("BTC","USDT","buy","0.1","BTC"))
    def test_query_estimate(self):
        print(self.ConvertAPI.estimate_quote("BTC", "USDT", "buy", "0.1", "BTC"))
    def test_convert_trade(self):
        print(self.ConvertAPI.convert_trade('quotersBTC-USDT16618704214351712','BTC',"USDT",'buy','0.1','BTC'))
    def test_get_convert_history(self):
        print(self.ConvertAPI.get_convert_history())
    '''


    #def test_query_estimate(self):
      #  print(self.ConvertAPI.estimate_quote("BTC", "USDT", "buy", "0.1", "BTC"))

if __name__ == '__main__':
    unittest.main()
