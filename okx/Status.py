from .client import Client
from .consts import *


class StatusAPI(Client):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain = 'https://www.okx.com',debug = True):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain,debug)

    def status(self, state=''):
        params = {'state': state}
        return self._request_with_params(GET, STATUS, params)
