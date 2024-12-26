from .okxclient import OkxClient
from .consts import *


class FDBrokerAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain = 'https://www.okx.com',debug = False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    def generate_rebate_details_download_link(self, begin ='', end = ''):
        params = {'begin': begin, 'end': end}
        return self._request_with_params(POST, FD_REBATE_PER_ORDERS, params)

    def get_rebate_details_download_link(self, type = '', begin = '', end = ''):
        params = {'type': type, 'begin': begin, 'end': end}
        return self._request_with_params(GET, FD_GET_REBATE_PER_ORDERS, params)
