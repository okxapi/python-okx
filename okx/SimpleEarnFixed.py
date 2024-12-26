from okx.consts import GET, LENDING_OFFERS, LENDING_APY_HISTORY, PENDING_LENDING_VOLUME, PLACE_LENDING_ORDER, POST, \
    AMEND_LENDING_ORDER, LENDING_ORDERS_LIST, LENDING_SUB_ORDERS
from okx.okxclient import OkxClient


class SimpleEarnFixedAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1',
                 domain='https://www.okx.com', debug=False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    def get_lending_offers(self, ccy=None, term=None):
        params = {}
        if ccy is not None:
            params['ccy'] = ccy
        if term is not None:
            params['term'] = term
        return self._request_with_params(GET, LENDING_OFFERS, params)

    def get_lending_apy_history(self, ccy=None, term=None):
        params = {}
        if ccy is not None:
            params['ccy'] = ccy
        if term is not None:
            params['term'] = term
        return self._request_with_params(GET, LENDING_APY_HISTORY, params)

    def get_pending_lending_volume(self, ccy=None, term=None):
        params = {}
        if ccy is not None:
            params['ccy'] = ccy
        if term is not None:
            params['term'] = term
        return self._request_with_params(GET, PENDING_LENDING_VOLUME, params)

    def place_lending_order(self, ccy=None, amt=None, rate=None, term=None, autoRenewal=False):
        params = {}
        if ccy is not None:
            params['ccy'] = ccy
        if amt is not None:
            params['amt'] = amt
        if rate is not None:
            params['rate'] = rate
        if term is not None:
            params['term'] = term
        if autoRenewal:
            params['autoRenewal'] = autoRenewal
        return self._request_with_params(POST, PLACE_LENDING_ORDER, params)
    def amend_lending_order(self, ordId=None, changeAmt=None, rate=None,autoRenewal=False):
        params = {}
        if ordId is not None:
            params['ordId'] = ordId
        if changeAmt is not None:
            params['amt'] = changeAmt
        if rate is not None:
            params['rate'] = rate
        params['autoRenewal'] = autoRenewal
        return self._request_with_params(POST, AMEND_LENDING_ORDER, params)

    def get_lending_orders_list(self, ordId = None,ccy=None, state=None, after=None,before=None,limit=None):
        params = {}
        if ordId is not None:
            params['ordId'] = ordId
        if ccy is not None:
            params['ccy'] = ccy
        if state is not None:
            params['state'] = state
        if after is not None:
            params['after'] = after
        if before is not None:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, LENDING_ORDERS_LIST, params)

    def get_lending_sub_orders(self, ordId = None, state=None, after=None,before=None,limit=None):
        params = {}
        if ordId is not None:
            params['ordId'] = ordId
        if state is not None:
            params['state'] = state
        if after is not None:
            params['after'] = after
        if before is not None:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, LENDING_SUB_ORDERS, params)




