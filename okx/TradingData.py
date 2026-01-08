from .okxclient import OkxClient
from .consts import *


class TradingDataAPI(OkxClient):

    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain = 'https://www.okx.com',debug = False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)


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

    def get_open_interest_history(self, instId, period=None, begin=None, end=None, limit=None):
        """
        Get contract open interest history
        Retrieve the contract open interest statistics of futures and perp.
        Rate limit: 10 requests per 2 seconds
        Rate limit rule: IP + Instrument ID
        
        :param instId: Instrument ID, e.g. BTC-USDT-SWAP. Only applicable to FUTURES, SWAP
        :param period: Bar size, the default is 5m, e.g. [5m/15m/30m/1H/2H/4H]
        :param begin: Return records newer than the requested ts
        :param end: Pagination of data to return records earlier than the requested ts
        :param limit: Number of results per request. The maximum is 100. The default is 100
        :return: API response
        """
        params = {'instId': instId}
        if period is not None:
            params['period'] = period
        if begin is not None:
            params['begin'] = begin
        if end is not None:
            params['end'] = end
        if limit is not None:
            params['limit'] = limit
        return self._request_with_params(GET, CONTRACTS_OPEN_INTEREST_HISTORY, params)







