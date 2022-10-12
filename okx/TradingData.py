from .client import Client
from .consts import *


class TradingDataAPI(Client):

    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain = 'https://www.okx.com',debug = True):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain,debug)


    def get_support_coin(self):
        return self._request_without_params(GET, SUPPORT_COIN)

    def get_taker_volume(self, ccy, instType, begin='', end='', period=''):
        params = {'ccy': ccy, 'instType': instType, 'begin': begin, 'end': end, 'period': period}
        return self._request_with_params(GET, TAKER_VOLUME, params)

    def get_margin_lending_ratio(self, ccy, begin='', end='', period=''):
        params = {'ccy': ccy, 'begin': begin, 'end': end, 'period': period}
        return self._request_with_params(GET, MARGIN_LENDING_RATIO, params)

    def get_long_short_ratio(self, ccy, begin='', end='', period=''):
        params = {'ccy': ccy, 'begin': begin, 'end': end, 'period': period}
        return self._request_with_params(GET, LONG_SHORT_RATIO, params)

    def get_contracts_interest_volume(self, ccy, begin='', end='', period=''):
        params = {'ccy': ccy, 'begin': begin, 'end': end, 'period': period}
        return self._request_with_params(GET, CONTRACTS_INTEREST_VOLUME, params)

    def get_options_interest_volume(self, ccy, period=''):
        params = {'ccy': ccy, 'period': period}
        return self._request_with_params(GET, OPTIONS_INTEREST_VOLUME, params)

    def get_put_call_ratio(self, ccy, period=''):
        params = {'ccy': ccy, 'period': period}
        return self._request_with_params(GET, PUT_CALL_RATIO, params)

    def get_interest_volume_expiry(self, ccy, period=''):
        params = {'ccy': ccy, 'period': period}
        return self._request_with_params(GET, OPEN_INTEREST_VOLUME_EXPIRY, params)

    def get_interest_volume_strike(self, ccy, expTime, period=''):
        params = {'ccy': ccy, 'expTime': expTime, 'period': period}
        return self._request_with_params(GET, INTEREST_VOLUME_STRIKE, params)

    def get_taker_block_volume(self, ccy, period=''):
        params = {'ccy': ccy, 'period': period}
        return self._request_with_params(GET, TAKER_FLOW, params)







