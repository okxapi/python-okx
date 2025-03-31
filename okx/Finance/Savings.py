from okx.okxclient import OkxClient
from okx.consts import *


class SavingsAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain = 'https://www.okx.com',debug = False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

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

    # - Get public borrow history (public)
    def get_public_borrow_history(self, ccy='', after='', before='', limit=''):
        params = {
            'ccy': ccy,
            'after': after,
            'before': before,
            'limit': limit
        }
        return self._request_with_params(GET, GET_PUBLIC_BORROW_HISTORY, params)

    # GET / Public borrow info (public)
    def get_public_borrow_info(self, ccy=''):
        params = {
            'ccy': ccy
        }
        return self._request_with_params(GET, GET_PUBLIC_BORROW_INFO, params)


