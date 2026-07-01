from .okxclient import OkxClient
from .consts import *


class DualInvestAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain='https://www.okx.com', debug=False, proxy=None):  # NOSONAR - '-1' is the SDK-wide "no credential supplied" sentinel (auth is gated on api_key != '-1' in OkxClient), not a hard-coded secret
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    # GET /api/v5/dualinvest/currency-pairs
    def get_currency_pairs(self):
        return self._request_without_params(GET, DUAL_INVEST_CURRENCY_PAIRS)

    # GET /api/v5/dualinvest/product-info
    def get_product_info(self):
        return self._request_without_params(GET, DUAL_INVEST_PRODUCT_INFO)

    # POST /api/v5/dualinvest/request-quote
    def request_quote(self, ccy='', investCcy='', quoteCcy='', side='', sz=''):
        params = {'ccy': ccy, 'investCcy': investCcy, 'quoteCcy': quoteCcy, 'side': side, 'sz': sz}
        return self._request_with_params(POST, DUAL_INVEST_REQUEST_QUOTE, params)

    # POST /api/v5/dualinvest/trade
    def trade(self, quoteId='', ccy='', investCcy='', quoteCcy='', side='', sz=''):
        params = {'quoteId': quoteId, 'ccy': ccy, 'investCcy': investCcy, 'quoteCcy': quoteCcy, 'side': side, 'sz': sz}
        return self._request_with_params(POST, DUAL_INVEST_TRADE, params)

    # POST /api/v5/dualinvest/request-redeem-quote
    def request_redeem_quote(self, ordId='', ccy='', sz=''):
        params = {'ordId': ordId, 'ccy': ccy, 'sz': sz}
        return self._request_with_params(POST, DUAL_INVEST_REQUEST_REDEEM_QUOTE, params)

    # POST /api/v5/dualinvest/redeem
    def redeem(self, quoteId='', ordId='', ccy='', sz=''):
        params = {'quoteId': quoteId, 'ordId': ordId, 'ccy': ccy, 'sz': sz}
        return self._request_with_params(POST, DUAL_INVEST_REDEEM, params)

    # GET /api/v5/dualinvest/order-state
    def get_order_state(self, ordId=''):
        params = {'ordId': ordId}
        return self._request_with_params(GET, DUAL_INVEST_ORDER_STATE, params)

    # GET /api/v5/dualinvest/order-history
    def get_order_history(self, ccy='', after='', before='', limit=''):
        params = {'ccy': ccy, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, DUAL_INVEST_ORDER_HISTORY, params)
