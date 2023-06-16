from .client import Client
from .consts import *


class SubAccountAPI(Client):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain = 'https://www.okx.com',debug = True):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain,debug)

    def get_account_balance(self, subAcct):
        params = {"subAcct": subAcct}
        return self._request_with_params(GET, BALANCE, params)

    def bills(self, ccy='', type='', subAcct='', after='', before='', limit=''):
        params = {"ccy": ccy, 'type': type, 'subAcct': subAcct, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, BILLs, params)


    def reset_subaccount_apikey(self, subAcct,apiKey, label='', perm='', ip='-1'):
        params = {'subAcct': subAcct, 'apiKey': apiKey}

        if ip != '-1':
            params['ip'] = ip
        if label != '':
            params['label'] = label
        if perm != '':
            params['perm'] = perm
        #params = {'subAcct': subAcct, 'label': label, 'apiKey': apiKey, 'perm': perm, 'ip': ip}
        return self._request_with_params(POST, RESET, params)


    def get_subaccount_list(self, enable='', subAcct='', after='', before='', limit=''):
        params = {'enable': enable, 'subAcct': subAcct, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, VIEW_LIST, params)

    def subAccount_transfer(self, ccy, amt, froms, to, fromSubAccount,toSubAccount,loanTrans='false',omitPosRisk = 'false'):
        params = {'ccy': ccy, 'amt': amt, 'from': froms, 'to': to, 'fromSubAccount': fromSubAccount, 'toSubAccount': toSubAccount,'loanTrans':loanTrans,'omitPosRisk':omitPosRisk}
        return self._request_with_params(POST, SUBACCOUNT_TRANSFER, params)

    #GET /api/v5/users/entrust-subaccount-list
    def get_entrust_subaccount_list(self,subAcct = ''):
        params = {
            'subAcct':subAcct
        }
        return self._request_with_params(GET, ENTRUST_SUBACCOUNT_LIST, params)

    #POST /api/v5/users/subaccount/set-transfer-out
    def set_permission_transfer_out(self,subAcct = '',canTransOut = ''):
        params = {
            'subAcct':subAcct,
            'canTransOut':canTransOut
        }
        return self._request_with_params(POST, SET_TRSNSFER_OUT, params)

    #GET /api/v5/asset/subaccount/balances
    def get_funding_balance(self,subAcct='',ccy=''):
        params = {
            'subAcct':subAcct,
            'ccy':ccy
        }
        return self._request_with_params(GET, GET_ASSET_SUBACCOUNT_BALANCE, params)

    # - Get the user's affiliate rebate information
    def get_the_user_affiliate_rebate_information(self, apiKey=''):
        params = {
            'apiKey': apiKey
        }
        return self._request_with_params(GET, GET_THE_USER_AFFILIATE_REBATE, params)

    # - Set sub_accounts VIP loan%
    def set_sub_accounts_VIP_loan(self, enable='', alloc=[]):
        params = {
            'enable': enable,
            'alloc': alloc
        }
        return self._request_with_params(POST, SET_SUB_ACCOUNTS_VIP_LOAN, params)

    # - Get sub_account borrow interest and limit
    def get_sub_account_borrow_interest_and_limit(self, subAcct='', ccy=''):
        params = {
            'subAcct': subAcct,
            'ccy': ccy
        }
        return self._request_with_params(GET, GET_SUB_ACCOUNT_BORROW_INTEREST_AND_LIMIT, params)
