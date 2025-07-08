from okx.okxclient import OkxClient
from okx.consts import *


class EthStakingAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain = 'https://www.okx.com',debug = False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    def eth_product_info(self):

        return self._request_without_params(GET, STACK_ETH_PRODUCT_INFO)

    def eth_purchase(self, amt=''):

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

    def eth_purchase_redeem_history(self, type='', status='', after='', before='', limit=''):

        params = {}
        if type != '':
            params['type'] = type
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
