from .okxclient import OkxClient
from .consts import *


class EarningAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain = 'https://www.okx.com',debug = False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    def get_offers(self,productId = '',protocolType = '',ccy = ''):
        params = {
            'productId':productId,
            'protocolType':protocolType,
            'ccy':ccy
        }
        return self._request_with_params(GET,STACK_DEFI_OFFERS,params)

    def purchase(self, productId='', investData=[], term='', tag=''):

        params = {
            'productId': productId,
            'investData': investData
        }
        if term != '':
            params['term'] = term
        if tag != '':
            params['tag'] = tag
        return self._request_with_params(POST, STACK_DEFI_PURCHASE, params)

    def redeem(self,ordId = '',protocolType = '',allowEarlyRedeem = ''):
        params = {
            'ordId':ordId,
            'protocolType':protocolType,
            'allowEarlyRedeem':allowEarlyRedeem
        }
        return self._request_with_params(POST,STACK_DEFI_REDEEM,params)

    def cancel(self,ordId = '',protocolType = ''):
        params = {
            'ordId':ordId,
            'protocolType':protocolType
        }
        return self._request_with_params(POST,STACK_DEFI_CANCEL,params)

    def get_activity_orders(self,productId = '',protocolType = '',ccy = '',state = ''):
        params = {
            'productId':productId,
            'protocolType':protocolType,
            'ccy':ccy,
            'state':state
        }
        return self._request_with_params(GET,STACK_DEFI_ORDERS_ACTIVITY,params)

    def get_orders_history(self,productId = '',protocolType = '',ccy = '',after = '',before = '',limit = ''):
        params = {
            'productId':productId,
            'protocolType':protocolType,
            'ccy':ccy,
            'after':after,
            'before':before,
            'limit':limit
        }
        return self._request_with_params(GET,STACK_DEFI_ORDERS_HISTORY,params)

    def eth_product_info(self):

        return self._request_without_params(GET, STACK_ETH_PRODUCT_INFO)
    
    def eth_purchase(self, amt):

        params = {
            'amt': amt,
        }
        return self._request_with_params(POST, STACK_ETH_PURCHASE, params)

    def eth_redeem(self, amt=''):

        params = {
            'amt': amt,
        }
        return self._request_with_params(POST, STACK_ETH_REDEEM, params)

    def eth_balance(self):

        params = {}
        return self._request_with_params(GET, STACK_ETH_BALANCE, params)

    def eth_purchase_redeem_history(self, type, status='', after='', before='', limit=''):

        params = {
            'type': type,
        }
        if status != '':
            params['status'] = status
        if after != '':
            params['after'] = after
        if before != '':
            params['before'] = before
        if limit != '':
            params['limit'] = limit
        return self._request_with_params(GET, STACK_ETH_PURCHASE_REDEEM_HISTORY, params)

    def eth_apy_history(self, days):

        params = {
            'days': days,
        }
        return self._request_with_params(GET, STACK_ETH_APY_HISTORY, params)

    def sol_purchase(self, amt):

        params = {
            'amt': amt,
        }
        return self._request_with_params(POST, STACK_SOL_PURCHASE, params)

    def sol_redeem(self, amt=''):

        params = {
            'amt': amt,
        }
        return self._request_with_params(POST, STACK_SOL_REDEEM, params)

    def sol_balance(self):

        params = {}
        return self._request_with_params(GET, STACK_SOL_BALANCE, params)

    def sol_purchase_redeem_history(self, type, status='', after='', before='', limit=''):

        params = {
            'type': type,
        }
        if status != '':
            params['status'] = status
        if after != '':
            params['after'] = after
        if before != '':
            params['before'] = before
        if limit != '':
            params['limit'] = limit
        return self._request_with_params(GET, STACK_SOL_PURCHASE_REDEEM_HISTORY, params)

    def sol_apy_history(self, days):

        params = {
            'days': days,
        }
        return self._request_with_params(GET, STACK_SOL_APY_HISTORY, params)

    # - Get saving balance
    def get_saving_balance(self, ccy=''):
        params = {
            'ccy': ccy
        }
        return self._request_with_params(GET, GET_SAVING_BALANCE, params)

    # - Savings purchase/redemption
    def savings_purchase_redemption(self, ccy='', amt='', side='', rate=''):

        params = {
            'ccy': ccy,
            'amt': amt,
            'side': side,
            'rate': rate
        }
        return self._request_with_params(POST, SAVING_PURCHASE_REDEMPTION, params)

    # - Set lending rate
    def set_lending_rate(self, ccy='', rate=''):
        params = {
            'ccy': ccy,
            'rate': rate
        }
        return self._request_with_params(POST, SET_LENDING_RATE, params)

    # - Get lending history
    def get_lending_history(self, ccy='', after='', before='', limit=''):
        params = {
            'ccy': ccy,
            'after': after,
            'before': before,
            'limit': limit
        }
        return self._request_with_params(GET, GET_LENDING_HISTORY, params)

    # - Get public borrow info (public)
    def get_public_borrow_info(self, ccy=''):
        params = {
            'ccy': ccy
        }
        return self._request_with_params(GET, GET_PUBLIC_BORROW_INFO, params)

    # - Get public borrow history (public)
    def get_public_borrow_history(self, ccy='', after='', before='', limit=''):
        params = {
            'ccy': ccy,
            'after': after,
            'before': before,
            'limit': limit
        }
        return self._request_with_params(GET, GET_PUBLIC_BORROW_HISTORY, params)
