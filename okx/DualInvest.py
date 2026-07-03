from .okxclient import OkxClient
from .consts import (
    GET,
    POST,
    DUAL_INVEST_CURRENCY_PAIRS,
    DUAL_INVEST_PRODUCT_INFO,
    DUAL_INVEST_REQUEST_QUOTE,
    DUAL_INVEST_TRADE,
    DUAL_INVEST_REQUEST_REDEEM_QUOTE,
    DUAL_INVEST_REDEEM,
    DUAL_INVEST_ORDER_STATE,
    DUAL_INVEST_ORDER_HISTORY,
)


class DualInvestAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain='https://www.okx.com', debug=False, proxy=None):  # NOSONAR - '-1' is the SDK-wide "no credential supplied" sentinel (auth is gated on api_key != '-1' in OkxClient), not a hard-coded secret
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    # GET /api/v5/finance/sfp/dcd/currency-pair
    def get_currency_pairs(self):
        return self._request_without_params(GET, DUAL_INVEST_CURRENCY_PAIRS)

    # GET /api/v5/finance/sfp/dcd/products
    def get_product_info(self, baseCcy='', quoteCcy='', optType=''):
        params = {'baseCcy': baseCcy, 'quoteCcy': quoteCcy, 'optType': optType}
        return self._request_with_params(GET, DUAL_INVEST_PRODUCT_INFO, params)

    # POST /api/v5/finance/sfp/dcd/quote
    def request_quote(self, productId='', notionalSz='', notionalCcy=''):
        params = {'productId': productId, 'notionalSz': notionalSz, 'notionalCcy': notionalCcy}
        return self._request_with_params(POST, DUAL_INVEST_REQUEST_QUOTE, params)

    # POST /api/v5/finance/sfp/dcd/trade
    def trade(self, quoteId=''):
        params = {'quoteId': quoteId}
        return self._request_with_params(POST, DUAL_INVEST_TRADE, params)

    # POST /api/v5/finance/sfp/dcd/redeem-quote
    def request_redeem_quote(self, ordId=''):
        params = {'ordId': ordId}
        return self._request_with_params(POST, DUAL_INVEST_REQUEST_REDEEM_QUOTE, params)

    # POST /api/v5/finance/sfp/dcd/redeem
    def redeem(self, ordId='', quoteId=''):
        params = {'ordId': ordId, 'quoteId': quoteId}
        return self._request_with_params(POST, DUAL_INVEST_REDEEM, params)

    # GET /api/v5/finance/sfp/dcd/order-status
    def get_order_state(self, ordId=''):
        params = {'ordId': ordId}
        return self._request_with_params(GET, DUAL_INVEST_ORDER_STATE, params)

    # GET /api/v5/finance/sfp/dcd/order-history
    def get_order_history(self, ordId='', productId='', uly='', state='',
                          beginId='', endId='', begin='', end='', limit=''):
        params = {'ordId': ordId, 'productId': productId, 'uly': uly, 'state': state,
                  'beginId': beginId, 'endId': endId, 'begin': begin, 'end': end, 'limit': limit}
        return self._request_with_params(GET, DUAL_INVEST_ORDER_HISTORY, params)
