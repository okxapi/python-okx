import json

import httpx

from . import consts as c, utils, exceptions

import time

import traceback

from httpx import _client

class Client(object):

    def __init__(self, api_key = '-1', api_secret_key = '-1', passphrase = '-1', use_server_time=False, flag='1', base_api = 'https://www.okx.com',debug = False):

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
            sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body), self.debug), self.API_SECRET_KEY)
            header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE, self.flag, self.debug)
        else:
            header = utils.get_header_no_sign(self.flag, self.debug)
        response = None
        if self.debug == True:
            print('domain:',self.domain)
            print('url:',request_path)
        if method == c.GET:
            response = self.client.get(request_path, headers=header)
        elif method == c.POST:
            response = self.client.post(request_path, data=body, headers=header)
        self.request_times += 1
        # print('request times:', self.request_times)
        if (self.request_times > 512):
            self.client.close()
            self.client._state = _client.ClientState.UNOPENED
            self.request_times = 0
            # print('close the current tcp connection while request times larger than 512.')
        return response

    def _request_until_success(self, method, request_path, params):
        response = ''
        retry_times = 0
        retry_times_max = 15
        while True:
            try:
                response = self._request(method, request_path, params)
                break
            except Exception as e:
                msg = traceback.format_exc()
                print(msg)
                retry_times += 1
                if retry_times > retry_times_max:
                    print('reach max retry times, exit loop.')
                    break
                print('http request failed, retry in 1 seconds ... retry times:', retry_times)
                time.sleep(1)
        if not str(response.status_code).startswith('2'):
            raise exceptions.OkxAPIException(response)
        return response.json()

    def _request_without_params(self, method, request_path):
        return self._request_with_params(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request_until_success(method, request_path, params)

    def _get_timestamp(self):
        request_path = base_api + c.SERVER_TIMESTAMP_URL
        response = self.client.get(request_path)
        if response.status_code == 200:
            return response.json()['ts']
        else:
            return ""
