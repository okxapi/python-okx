
import unittest
from okx import MarketData

'''
ORACLE = '/api/v5/market/open-oracle' #need to update? if it is open oracle
INDEX_COMPONENTS = '/api/v5/market/index-components' #need to add
EXCHANGE_RATE = '/api/v5/market/exchange-rate' #need to add
HISTORY_TRADES = '/api/v5/market/history-trades' #need to add
BLOCK_TICKERS = '/api/v5/market/block-tickers' #need to add
BLOCK_TICKER = '/api/v5/market/block-ticker'#need to add
BLOCK_TRADES = '/api/v5/market/block-trades'#need to add
'''

class MarketAPITest(unittest.TestCase):
    def setUp(self):
        api_key = 'ef06bf27-6a01-4797-b801-e3897031e45d'
        api_secret_key = 'D3620B2660203350EEE80FDF5BE0C960'
        passphrase = 'Beijing123'
        self.MarketApi = MarketData.MarketAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')
    '''
    
    def test_oracle(self):
        print(self.MarketApi.get_oracle())
    def test_index_component(self):
        print(self.MarketApi.get_index_components("BTC-USDT"))
    def test_exchange_rate(self):
        print(self.MarketApi.get_exchange_rate())
    def test_history_trades(self):
        print(self.MarketApi.get_history_trades("BTC-USDT"))
    def test_block_tickers(self):
        print(self.MarketApi.get_block_tickers("SPOT"))
    def test_block_ticker(self):
        print(self.MarketApi.get_block_ticker("BTC-USD-SWAP"))
    def test_block_trades(self):
        print(self.MarketApi.get_block_trades("BTC-USDT"))
    def test_get_tickers(self):
        print(self.MarketApi.get_tickers('SPOT'))
    def test_get_ticker(self):
        print(self.MarketApi.get_ticker('BTC-USD-SWAP'))
    def test_index_ticker(self):
        print(self.MarketApi.get_index_ticker('USDT'))
    def test_get_books(self):
        print(self.MarketApi.get_orderbook('BTC-USDT'))
    def test_get_candles(self):
        print(self.MarketApi.get_candlesticks('BTC-USDT'))
    def test_get_candles_history(self):
        print(self.MarketApi.get_history_candlesticks('BTC-USDT'))
    def test_get_index_candles(self):
        print(self.MarketApi.get_index_candlesticks('BTC-USD'))
    def test_get_market_price_candles(self):
        print(self.MarketApi.get_mark_price_candlesticks('BTC-USD-SWAP'))
    def test_get_trade(self):
        print(self.MarketApi.get_trades('BTC-USDT'))
    def test_get_history_trades(self):
        print(self.MarketApi.get_history_trades('BTC-USDT'))
    def test_get_platform_24_volume(self):
        print(self.MarketApi.get_volume())
    '''

    # def test_get_order_lite_book(self):
    #     print(self.MarketApi.get_order_lite_book(instId='BTC-USDT'))

    def test_get_option_trades(self):
        print(self.MarketApi.get_option_trades(instFamily='BTC-USD'))


if __name__ == "__main__":
    unittest.main()