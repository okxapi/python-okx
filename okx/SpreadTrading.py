from .okxclient import OkxClient
from .consts import *


class SpreadTradingAPI(OkxClient):

    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain = 'https://www.okx.com',debug = False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    # Place Order
    def place_order(self, sprdId='', clOrdId='', tag='', side='', ordType='', sz='', px=''):
        params = {'sprdId': sprdId, 'clOrdId': clOrdId, 'tag': tag, 'side': side, 'ordType': ordType, 'sz': sz,
                  'px': px}
        return self._request_with_params(POST, SPREAD_PLACE_ORDER, params)

    # Cancel Order
    def cancel_order(self,ordId='', clOrdId=''):
        params = {'ordId': ordId, 'clOrdId': clOrdId}
        return self._request_with_params(POST, SPREAD_CANCEL_ORDER, params)

    # Cancel All orders
    def cancel_all_orders(self, sprdId=''):
        params = {'sprdId': sprdId}
        return self._request_with_params(POST, SPREAD_CANCEL_ALL_ORDERS, params)

    # Get order details
    def get_order_details(self, ordId='', clOrdId=''):
        params = {'ordId': ordId, 'clOrdId': clOrdId}
        return self._request_with_params(GET, SPREAD_GET_ORDER_DETAILS, params)

    # Get active orders
    def get_active_orders(self, sprdId='', ordType='', state='', beginId='', endId='', limit=''):
        params = {'sprdId': sprdId, 'ordType': ordType, 'state': state, 'beginId': beginId, 'endId': endId, 'limit': limit}
        return self._request_with_params(GET, SPREAD_GET_ACTIVE_ORDERS, params)

    # Get orders (last 7 days)
    def get_orders(self, sprdId='', ordType='', state='', beginId='', endId='', begin='', end='', limit=''):
        params = {'sprdId': sprdId, 'ordType': ordType, 'state': state, 'beginId': beginId, 'endId': endId,
                  'begin': begin, 'end': end, 'limit': limit}
        return self._request_with_params(GET, SPREAD_GET_ORDERS, params)

    # Get trades (last 7 days)
    def get_trades(self, sprdId='', tradeId='', ordId='', beginId='', endId='', begin='', end='', limit=''):
        params = {'sprdId': sprdId, 'tradeId': tradeId, 'ordId': ordId, 'beginId': beginId, 'endId': endId,
                  'begin': begin, 'end': end, 'limit': limit}
        return self._request_with_params(GET, SPREAD_GET_TRADES, params)

    # Get Spreads (Public)
    def get_spreads(self, baseCcy='',instId='', sprdId='', state=''):
        params = {'baseCcy': baseCcy, 'instId': instId, 'sprdId': sprdId, 'state': state}
        return self._request_with_params(GET, SPREAD_GET_SPREADS, params)

    # Get order book (Public)
    def get_order_book(self, sprdId='', sz=''):
        params = {'sprdId': sprdId, 'sz': sz}
        return self._request_with_params(GET, SPREAD_GET_ORDER_BOOK, params)

    # Get ticker (Public)
    def get_ticker(self, sprdId=''):
        params = {'sprdId': sprdId}
        return self._request_with_params(GET, SPREAD_GET_TICKER, params)

    # Get public trades (Public)
    def get_public_trades(self, sprdId=''):
        params = {'sprdId': sprdId}
        return self._request_with_params(GET, SPREAD_GET_PUBLIC_TRADES, params)

