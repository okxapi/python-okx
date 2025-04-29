from okx.okxclient import OkxClient
from okx.consts import *


class FlexibleLoanAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1',
                 domain='https://www.okx.com', debug=False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    def borrow_currencies(self):
        return self._request_without_params(GET, FINANCE_BORROW_CURRENCIES)

    def collateral_assets(self, ccy=''):
        params = {}
        if ccy != '':
            params['ccy'] = ccy
        return self._request_with_params(GET, FINANCE_COLLATERAL_ASSETS, params)

    def max_loan(self, borrowCcy='', supCollateral=[]):
        params = {
            'borrowCcy': borrowCcy,
            'supCollateral': supCollateral,
        }
        return self._request_with_params(POST, FINANCE_MAX_LOAN, params)

    def max_collateral_redeem_amount(self, ccy=''):
        params = {}
        if ccy != '':
            params['ccy'] = ccy
        return self._request_with_params(GET, FINANCE_MAX_REDEEM, params)

    def adjust_collateral(self, type='', collateralCcy='', collateralAmt=''):
        params = {
            'type': type,
            'collateralCcy': collateralCcy,
            'collateralAmt': collateralAmt,
        }
        return self._request_with_params(POST, FINANCE_ADJUST_COLLATERAL, params)

    def loan_info(self):
        return self._request_without_params(GET, FINANCE_LOAN_INFO)

    def loan_history(self, type='', after='', before='', limit=''):
        params = {}
        if type != '':
            params['type'] = type
        if after != '':
            params['after'] = after
        if before != '':
            params['before'] = before
        if limit != '':
            params['limit'] = limit
        return self._request_with_params(GET, FINANCE_LOAN_HISTORY, params)

    def interest_accrued(self, ccy='', after='', before='', limit=''):
        params = {}
        if ccy != '':
            params['ccy'] = ccy
        if after != '':
            params['after'] = after
        if before != '':
            params['before'] = before
        if limit != '':
            params['limit'] = limit
        return self._request_with_params(GET, FINANCE_INTEREST_ACCRUED, params)
