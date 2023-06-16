from .client import Client
from .consts import *


class FundingAPI(Client):


    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain = 'https://www.okx.com',debug = True):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain,debug)

    # Get Deposit Address
    def get_deposit_address(self, ccy):
        params = {'ccy': ccy}
        return self._request_with_params(GET, DEPOSIT_ADDRESS, params)

    # Get Transfer State
    def transfer_state(self, transId,type=''):
        params = {'transId': transId, 'type': type}
        return self._request_with_params(GET, TRANSFER_STATE, params)

    # Get Balance
    def get_balances(self, ccy=''):
        params = {'ccy': ccy}
        return self._request_with_params(GET, GET_BALANCES, params)

    # Get Account Configuration
    def funds_transfer(self, ccy, amt, from_, to, type='0', subAcct='', instId='', toInstId='',loanTrans=''):
        params = {'ccy': ccy, 'amt': amt, 'from': from_, 'to': to, 'type': type, 'subAcct': subAcct, 'instId': instId,
                  'toInstId': toInstId,'loanTrans':loanTrans}
        return self._request_with_params(POST, FUNDS_TRANSFER, params)

    # Withdrawal
    def withdrawal(self, ccy, amt, dest, toAddr, fee, chain='', areaCode='', clientId=''):
        params = {'ccy': ccy, 'amt': amt, 'dest': dest, 'toAddr': toAddr, 'fee': fee, 'chain': chain,
                  'areaCode': areaCode, 'clientId': clientId}
        return self._request_with_params(POST, WITHDRAWAL_COIN, params)

    # Get Deposit History
    def get_deposit_history(self, ccy='', state='', after='', before='', limit='', txId='', depId='', fromWdId=''):
        params = {'ccy': ccy, 'state': state, 'after': after, 'before': before, 'limit': limit, 'txId': txId,
                  'depId': depId, 'fromWdId': fromWdId}
        return self._request_with_params(GET, DEPOSIT_HISTORIY, params)

    # Get Withdrawal History
    def get_withdrawal_history(self, ccy='', wdId='', state='', after='', before='', limit='',txId=''):
        params = {'ccy': ccy, 'wdId': wdId, 'state': state, 'after': after, 'before': before, 'limit': limit,'txId':txId}
        return self._request_with_params(GET, WITHDRAWAL_HISTORIY, params)

    # Get Currencies
    def get_currencies(self, ccy=''):
        params = {'ccy': ccy}
        return self._request_with_params(GET, CURRENCY_INFO, params)

    # PiggyBank Purchase/Redemption
    def purchase_redempt(self, ccy, amt, side, rate):
        params = {'ccy': ccy, 'amt': amt, 'side': side,'rate':rate}
        return self._request_with_params(POST, PURCHASE_REDEMPT, params)

    # Get Withdrawal History
    def get_bills(self, ccy='', type='', after='', before='', limit=''):
        params = {'ccy': ccy, 'type': type, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, BILLS_INFO, params)


    #Get Deposit Lightning
    def get_deposit_lightning(self, ccy,amt,to=""):
        params = {'ccy':ccy,'amt':amt}
        if to:
            params = {'to':to}
        return self._request_with_params(GET, DEPOSIT_LIGHTNING, params)

    # Withdrawal Lightning
    def withdrawal_lightning(self, ccy,invoice,memo=''):
        params = {'ccy':ccy, 'invoice':invoice, 'memo':memo}
        return self._request_with_params(POST, WITHDRAWAL_LIGHTNING, params)

    # POST SET LENDING RATE
    def set_lending_rate(self, ccy, rate):
        params = {'ccy': ccy, 'rate': rate}
        return self._request_with_params(POST, SET_LENDING_RATE, params)

    # GET LENDING HISTORY
    def get_lending_history(self, ccy='', before='', after='', limit='' ):
        params = {'ccy': ccy, 'after': after, 'before': before, 'limit': limit }
        return self._request_with_params(GET, LENDING_HISTORY, params)

    # GET LENDING RATE HISTORY
    def get_lending_rate_history(self, ccy='',after = '',before = '',limit = '' ):
        params = {'ccy': ccy,'after':after,'before':before,'limit':limit}
        return self._request_with_params(GET, LENDING_RATE_HISTORY, params)

    # GET LENDING RATE SUMMARY
    def get_lending_rate_summary(self, ccy=''):
        params = {'ccy': ccy}
        return self._request_with_params(GET, LENDING_RATE_SUMMARY, params)


    #POST /api/v5/asset/cancel-withdrawal
    def cancel_withdrawal(self,wdId = ''):
        params = {
            'wdId':wdId
        }
        return self._request_with_params(POST, CANCEL_WITHDRAWAL, params)

    #POST /api/v5/asset/convert-dust-assets
    def convert_dust_assets(self,ccy = []):
        params = {
            'ccy':ccy
        }
        return self._request_with_params(POST, CONVERT_DUST_ASSETS, params)

    #GET /api/v5/asset/asset-valuation
    def get_asset_valuation(self,ccy = ''):
        params = {
            'ccy':ccy
        }
        return self._request_with_params(GET, ASSET_VALUATION, params)

    #GET / api / v5 / asset / saving - balance
    def get_saving_balance(self,ccy = ''):
        params = {
            'ccy':ccy
        }
        return self._request_with_params(GET, GET_SAVING_BALANCE, params)

    #Get non-tradable assets
    def get_non_tradable_assets(self, ccy=''):
        params = {
            'ccy': ccy
        }
        return self._request_with_params(GET, GET_NON_TRADABLE_ASSETS, params)

    #Get deposit withdraw status
    def get_deposit_withdraw_status(self, wdId='', txId='', ccy='', to='', chain=''):
        params = {'wdId': wdId, 'txId': txId, 'ccy': ccy, 'to': to, 'chain': chain}
        return self._request_with_params(GET, GET_DEPOSIT_WITHDrAW_STATUS, params)

    #Get withdrawal history
    def get_withdrawal_history(self, ccy='', wdId='', clientId='', txId='', type='', state='', after='', before	='', limit=''):
        params = {'ccy': ccy, 'wdId': wdId, 'clientId': clientId, 'txId': txId, 'type': type, 'state': state, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, GET_WITHDRAWAL_HISTORY, params)

