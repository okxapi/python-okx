from okx.okxclient import OkxClient
from okx.consts import *


class OkusdAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1',
                 domain='https://www.okx.com', debug=False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    def get_account(self):
        return self._request_without_params(GET, OKUSD_ACCOUNT)

    def get_rate_history(self, limit='', begin='', end=''):
        params = {}
        if limit != '':
            params['limit'] = limit
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        return self._request_with_params(GET, OKUSD_RATE_HISTORY, params)

    def get_subscribe_history(self, limit='', begin='', end=''):
        params = {}
        if limit != '':
            params['limit'] = limit
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        return self._request_with_params(GET, OKUSD_SUBSCRIBE_HISTORY, params)

    def get_redeem_history(self, limit='', begin='', end='', type=''):
        params = {}
        if limit != '':
            params['limit'] = limit
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        if type != '':
            params['type'] = type
        return self._request_with_params(GET, OKUSD_REDEEM_HISTORY, params)

    def get_rewards_history(self, limit='', begin='', end=''):
        params = {}
        if limit != '':
            params['limit'] = limit
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        return self._request_with_params(GET, OKUSD_REWARDS_HISTORY, params)
