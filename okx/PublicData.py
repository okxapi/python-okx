from .client import Client
from .consts import *


class PublicAPI(Client):

    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain = 'https://www.okx.com',debug = True):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain,debug)

    # Get Instruments
    def get_instruments(self, instType, uly='', instId='',instFamily = ''):
        params = {'instType': instType, 'uly': uly, 'instId': instId,'instFamily':instFamily}
        return self._request_with_params(GET, INSTRUMENT_INFO, params)

    # Get Delivery/Exercise History
    def get_delivery_exercise_history(self, instType, uly = '', after='', before='', limit='',instFamily = ''):
        params = {'instType': instType, 'uly': uly, 'after': after, 'before': before, 'limit': limit,'instFamily':instFamily}
        return self._request_with_params(GET, DELIVERY_EXERCISE, params)

    # Get Open Interest
    def get_open_interest(self, instType, uly='', instId='' ,instFamily =''):
        params = {'instType': instType, 'uly': uly, 'instId': instId,'instFamily':instFamily}
        return self._request_with_params(GET, OPEN_INTEREST, params)

    # Get Funding Rate
    def get_funding_rate(self, instId):
        params = {'instId': instId}
        return self._request_with_params(GET, FUNDING_RATE, params)

    # Get Funding Rate History
    def funding_rate_history(self, instId, after='', before='', limit=''):
        params = {'instId': instId, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, FUNDING_RATE_HISTORY, params)

    # Get Limit Price
    def get_price_limit(self, instId):
        params = {'instId': instId}
        return self._request_with_params(GET, PRICE_LIMIT, params)

    # Get Option Market Data
    def get_opt_summary(self, uly = '', expTime='',instFamily=''):
        params = {'uly': uly, 'expTime': expTime,'instFamily':instFamily}
        return self._request_with_params(GET, OPT_SUMMARY, params)

    # Get Estimated Delivery/Excercise Price
    def get_estimated_price(self, instId):
        params = {'instId': instId}
        return self._request_with_params(GET, ESTIMATED_PRICE, params)

    # Get Discount Rate And Interest-Free Quota
    def discount_interest_free_quota(self, ccy=''):
        params = {'ccy': ccy}
        return self._request_with_params(GET, DICCOUNT_INTETEST_INFO, params)

    # Get System Time
    def get_system_time(self):
        return self._request_without_params(GET, SYSTEM_TIME)

    # Get Mark Price
    def get_mark_price(self, instType, uly='', instId='',instFamily = ''):
        params = {'instType': instType, 'uly': uly, 'instId': instId,'instFamily':instFamily}
        return self._request_with_params(GET, MARK_PRICE, params)

    # Get Tier
    def get_position_tiers(self, instType, tdMode, uly='', instId='', ccy='', tier='',instFamily =''):
        params = {'instType': instType, 'tdMode': tdMode, 'uly': uly, 'instId': instId, 'ccy': ccy, 'tier': tier,'instFamily':instFamily}
        return self._request_with_params(GET, TIER, params)

    #GET /api/v5/public/interest-rate-loan-quota
    def get_interest_rate_loan_quota(self):
        return self._request_without_params(GET,INTEREST_LOAN)

    #GET /api/v5/public/vip-interest-rate-loan-quota
    def get_vip_interest_rate_loan_quota(self):
        return self._request_without_params(GET, VIP_INTEREST_RATE_LOAN_QUOTA)

    #GET /api/v5/public/underlying
    def get_underlying(self,instType = ''):
        params = {
            'instType':instType
        }
        return self._request_with_params(GET, UNDERLYING, params)

    #GET /api/v5/public/insurance-fund
    def get_insurance_fund(self,instType = '',type = '',uly = '',ccy='',before = '',after = '',limit = '',instFamily=''):
        params = {
            'instType':instType,
            'type':type,
            'uly':uly,
            'ccy':ccy,
            'before':before,
            'after':after,
            'limit':limit,
            'instFamily':instFamily
        }
        return self._request_with_params(GET, INSURANCE_FUND, params)

    #GET /api/v5/public/convert-contract-coin
    def get_convert_contract_coin(self,type = '',instId = '',sz = '',px = '',unit = ''):
        params = {
            'type':type,
            'instId':instId,
            'sz':sz,
            'px':px,
            'unit':unit
        }
        return self._request_with_params(GET, CONVERT_CONTRACT_COIN, params)

    # Get option tickBands
    def get_option_tickBands(self, instType='', instFamily=''):
        params = {
            'instType': instType,
            'instFamily': instFamily
        }
        return self._request_with_params(GET, GET_OPTION_TICKBANDS, params)

    # Get option trades
    def get_option_trades(self, instId='', instFamily='', optType=''):
        params = {
            'instId': instId,
            'instFamily': instFamily,
            'optType': optType
        }
        return self._request_with_params(GET, GET_OPTION_TRADES, params)
