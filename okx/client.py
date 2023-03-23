import json
import time
import traceback

import httpx
from httpx import _client

from . import consts as c, utils


class Client(object):

    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1',
                 base_api=c.DOMAIN, debug=False):

        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key
        self.PASSPHRASE = passphrase
        self.use_server_time = use_server_time
        self.flag = flag
        self.domain = base_api
        self.debug = debug
        self.request_times = 0
        self.client = httpx.Client(base_url=base_api, http2=True, verify=False, timeout=None)

    def _request(self, method, request_path, params):
        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        timestamp = utils.get_timestamp()
        if self.use_server_time:
            timestamp = self._get_timestamp()
        body = json.dumps(params) if method == c.POST else ""
        if self.API_KEY != '-1':
            sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body), self.debug),
                              self.API_SECRET_KEY)
            header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE, self.flag, self.debug)
        else:
            header = utils.get_header_no_sign(self.flag, self.debug)
        response = None
        if self.debug:
            print('domain:', self.domain)
            print('url:', request_path)
        if method == c.GET:
            response = self.client.get(request_path, headers=header)
        elif method == c.POST:
            response = self.client.post(request_path, data=body, headers=header)
        self.request_times += 1
        if self.request_times > 512:
            self.client.close()
            self.client._state = _client.ClientState.UNOPENED
            self.request_times = 0
        return response

    def _request_until_success(self, method, request_path, params):
        response = ''
        retry_times = 0
        while True:
            try:
                response = self._request(method, request_path, params)
                if not str(response.status_code).startswith('2'):
                    print('response.status_code:', response.status_code)
                    print('response.json.code:', response.json()['code'])
                    print('response.json.msg:', response.json()['msg'])
                    time.sleep(1)
                    continue
                break
            except Exception as e:
                traceback.format_exc()
                print(e)
                retry_times += 1
                print('http request retry in 1 seconds, retry times:', retry_times)
                time.sleep(1)
        return response.json()

    def _request_without_params(self, method, request_path):
        return self._request_with_params(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request_until_success(method, request_path, params)

    def _get_timestamp(self):
        request_path = self.domain + c.SERVER_TIMESTAMP_URL
        response = self.client.get(request_path)
        if response.status_code == 200:
            return response.json()['ts']
        else:
            return ""
