from .consts import *
from .okxclient import OkxClient


class AccountAPI(OkxClient):

    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1',
                 domain='https://www.okx.com', debug=False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    # Get Positions
    def get_position_risk(self, instType=''):
        params = {}
        if instType:
            params['instType'] = instType
        return self._request_with_params(GET, POSITION_RISK, params)

    # Get Balance
    def get_account_balance(self, ccy=''):
        params = {}
        if ccy:
            params['ccy'] = ccy
        return self._request_with_params(GET, ACCOUNT_INFO, params)

    # Get Positions
    def get_positions(self, instType='', instId=''):
        params = {'instType': instType, 'instId': instId}
        return self._request_with_params(GET, POSITION_INFO, params)

    def position_builder(self, acctLv=None,inclRealPosAndEq=False, lever=None, greeksType=None, simPos=None,
                         simAsset=None):
        params = {}
        if acctLv is not None:
            params['acctLv'] = acctLv
        if inclRealPosAndEq is not None:
            params['inclRealPosAndEq'] = inclRealPosAndEq
        if lever is not None:
            params['spotOffsetType'] = lever
        if greeksType is not None:
            params['greksType'] = greeksType
        if simPos is not None:
            params['simPos'] = simPos
        if simAsset is not None:
            params['simAsset'] = simAsset
        return self._request_with_params(POST, POSITION_BUILDER, params)

    # Get Bills Details (recent 7 days)
    def get_account_bills(self, instType='', ccy='', mgnMode='', ctType='', type='', subType='', after='', before='',
                          limit=''):
        params = {'instType': instType, 'ccy': ccy, 'mgnMode': mgnMode, 'ctType': ctType, 'type': type,
                  'subType': subType, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, BILLS_DETAIL, params)

    # Get Bills Details (recent 3 months)
    def get_account_bills_archive(self, instType='', ccy='', mgnMode='', ctType='', type='', subType='', after='',
                                  before='',
                                  limit='', begin='', end=''):
        params = {'instType': instType, 'ccy': ccy, 'mgnMode': mgnMode, 'ctType': ctType, 'type': type,
                  'subType': subType, 'after': after, 'before': before, 'limit': limit, 'begin': begin, 'end': end}
        return self._request_with_params(GET, BILLS_ARCHIVE, params)

    # Get Account Configuration
    def get_account_config(self):
        return self._request_without_params(GET, ACCOUNT_CONFIG)

    # Get Account Configuration
    def set_position_mode(self, posMode):
        params = {'posMode': posMode}
        return self._request_with_params(POST, POSITION_MODE, params)

    # Get Account Configuration
    def set_leverage(self, lever, mgnMode, instId='', ccy='', posSide=''):
        params = {'lever': lever, 'mgnMode': mgnMode, 'instId': instId, 'ccy': ccy, 'posSide': posSide}
        return self._request_with_params(POST, SET_LEVERAGE, params)

    # Get Maximum Tradable Size For Instrument
    def get_max_order_size(self, instId, tdMode, ccy='', px=''):
        params = {'instId': instId, 'tdMode': tdMode, 'ccy': ccy, 'px': px}
        return self._request_with_params(GET, MAX_TRADE_SIZE, params)

    # Get Maximum Available Tradable Amount
    def get_max_avail_size(self, instId, tdMode, ccy='', reduceOnly='', unSpotOffset='', quickMgnType=''):
        params = {'instId': instId, 'tdMode': tdMode, 'ccy': ccy, 'reduceOnly': reduceOnly,
                  'unSpotOffset': unSpotOffset, 'quickMgnType': quickMgnType}
        return self._request_with_params(GET, MAX_AVAIL_SIZE, params)

    # Increase / Decrease margin
    def adjustment_margin(self, instId, posSide, type, amt, loanTrans=''):
        params = {'instId': instId, 'posSide': posSide, 'type': type, 'amt': amt, 'loanTrans': loanTrans}
        return self._request_with_params(POST, ADJUSTMENT_MARGIN, params)

    # Get Leverage
    def get_leverage(self, mgnMode, ccy='', instId=''):
        params = {'instId': instId, 'mgnMode': mgnMode, 'ccy': ccy}
        return self._request_with_params(GET, GET_LEVERAGE, params)

    # Get instruments
    def get_instruments(self, instType='', ugly='', instFamily='', instId=''):
        params = {'instType': instType, 'ugly': ugly, 'instFamily': instFamily, 'instId': instId}
        return self._request_with_params(GET, GET_INSTRUMENTS, params)

    # Get the maximum loan of isolated MARGIN
    def get_max_loan(self, instId, mgnMode, mgnCcy=''):
        params = {'instId': instId, 'mgnMode': mgnMode, 'mgnCcy': mgnCcy}
        return self._request_with_params(GET, MAX_LOAN, params)

    # Get Fee Rates
    def get_fee_rates(self, instType, instId='', uly='', category='', instFamily=''):
        params = {'instType': instType, 'instId': instId, 'uly': uly, 'category': category, 'instFamily': instFamily}
        return self._request_with_params(GET, FEE_RATES, params)

    # Get interest-accrued
    def get_interest_accrued(self, instId='', ccy='', mgnMode='', after='', before='', limit=''):
        params = {'instId': instId, 'ccy': ccy, 'mgnMode': mgnMode, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, INTEREST_ACCRUED, params)

    # Get interest-accrued
    def get_interest_rate(self, ccy=''):
        params = {'ccy': ccy}
        return self._request_with_params(GET, INTEREST_RATE, params)

    # Set Greeks (PA/BS)
    def set_greeks(self, greeksType):
        params = {'greeksType': greeksType}
        return self._request_with_params(POST, SET_GREEKS, params)

    # Set Isolated Mode
    def set_isolated_mode(self, isoMode, type):
        params = {'isoMode': isoMode, 'type': type}
        return self._request_with_params(POST, ISOLATED_MODE, params)

    # Get Maximum Withdrawals
    def get_max_withdrawal(self, ccy=''):
        params = {'ccy': ccy}
        return self._request_with_params(GET, MAX_WITHDRAWAL, params)

    # Get borrow repay
    def borrow_repay(self, ccy='', side='', amt='', ordId=''):
        params = {'ccy': ccy, 'side': side, 'amt': amt, 'ordId': ordId}
        return self._request_with_params(POST, BORROW_REPAY, params)

    # Get borrow repay history
    def get_borrow_repay_history(self, ccy='', after='', before='', limit=''):
        params = {'ccy': ccy, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, BORROW_REPAY_HISTORY, params)

    # Get Obtain borrowing rate and limit
    def get_interest_limits(self, type='', ccy=''):
        params = {'type': type, 'ccy': ccy}
        return self._request_with_params(GET, INTEREST_LIMITS, params)

    # Get Simulated Margin
    def get_simulated_margin(self, instType='', inclRealPos=True, spotOffsetType='', simPos=[]):
        params = {'instType': instType, 'inclRealPos': inclRealPos, 'spotOffsetType': spotOffsetType, 'simPos': simPos}
        return self._request_with_params(POST, SIMULATED_MARGIN, params)

    # Get  Greeks
    def get_greeks(self, ccy=''):
        params = {'ccy': ccy}
        return self._request_with_params(GET, GREEKS, params)

    # GET /api/v5/account/risk-state
    def get_account_position_risk(self):
        return self._request_without_params(GET, ACCOUNT_RISK)

    # GET /api/v5/account/positions-history
    def get_positions_history(self, instType='', instId='', mgnMode='', type='', posId='', after='', before='',
                              limit=''):
        params = {
            'instType': instType,
            'instId': instId,
            'mgnMode': mgnMode,
            'type': type,
            'posId': posId,
            'after': after,
            'before': before,
            'limit': limit
        }
        return self._request_with_params(GET, POSITIONS_HISTORY, params)

    # GET /api/v5/account/position-tiers
    def get_account_position_tiers(self, instType='', uly='', instFamily=''):
        params = {
            'instType': instType,
            'uly': uly,
            'instFamily': instFamily
        }
        return self._request_with_params(GET, GET_PM_LIMIT, params)

    # - Get VIP interest accrued data
    def get_VIP_interest_accrued_data(self, ccy='', ordId='', after='', before='', limit=''):
        params = {'ccy': ccy, 'ordId': ordId, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, GET_VIP_INTEREST_ACCRUED_DATA, params)

    # - Get VIP interest deducted data
    def get_VIP_interest_deducted_data(self, ccy='', ordId='', after='', before='', limit=''):
        params = {'ccy': ccy, 'ordId': ordId, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, GET_VIP_INTEREST_DEDUCTED_DATA, params)

    # - Get VIP loan order list
    def get_VIP_loan_order_list(self, ordId='', state='', ccy='', after='', before='', limit=''):
        params = {'ordId': ordId, 'state': state, 'ccy': ccy, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, GET_VIP_LOAN_ORDER_LIST, params)

    # - Get VIP loan order detail
    def get_VIP_loan_order_detail(self, ccy='', ordId='', after='', before='', limit=''):
        params = {'ccy': ccy, 'ordId': ordId, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, GET_VIP_LOAN_ORDER_DETAIL, params)

    # - Set risk offset type
    def set_risk_offset_typel(self, type=''):
        params = {'type': type}
        return self._request_with_params(POST, SET_RISK_OFFSET_TYPE, params)

    # - Set auto loan
    def set_auto_loan(self, autoLoan=''):
        params = {
            'autoLoan': autoLoan
        }
        return self._request_with_params(POST, SET_AUTO_LOAN, params)

    # - Set auto loan
    def set_account_level(self, acctLv):
        params = {
            'acctLv': acctLv
        }
        return self._request_with_params(POST, SET_ACCOUNT_LEVEL, params)

    # - Activate option
    def activate_option(self):
        return self._request_without_params(POST, ACTIVSTE_OPTION)

    def get_fix_loan_borrowing_limit(self):
        return self._request_without_params(GET, BORROWING_LIMIT)

    def get_fix_loan_borrowing_quote(self, type=None, ccy=None, amt=None, maxRate=None, term=None, ordId=None):
        params = {}
        if type is not None:
            params['type'] = type
        if ccy is not None:
            params['ccy'] =ccy
        if amt is not None:
            params['amt'] = amt
        if maxRate is not None:
            params['maxRate'] = maxRate
        if term is not None:
            params['term'] = term
        if ordId is not None:
            params['ordId'] = ordId
        return self._request_with_params(GET, BORROWING_QUOTE, params)

    def place_fix_loan_borrowing_order(self, ccy=None, amt=None, maxRate=None, term=None, reborrow=False, reborrowRate=None):
        params = {}
        if ccy is not None:
            params['ccy'] =ccy
        if amt is not None:
            params['amt'] = amt
        if maxRate is not None:
            params['maxRate'] = maxRate
        if term is not None:
            params['term'] = term
        if reborrow is not None:
            params['reborrow'] = reborrow
        if reborrowRate is not None:
            params['reborrowRate'] = reborrowRate
        return self._request_with_params(POST, PLACE_BORROWING_ORDER, params)

    def amend_fix_loan_borrowing_order(self, ordId=None, reborrow=None, renewMaxRate=None):
        params = {}
        if ordId is not None:
            params['ordId'] = ordId
        if reborrow is not None:
            params['reborrow'] = reborrow
        if renewMaxRate is not None:
            params['renewMaxRate'] = renewMaxRate
        return self._request_with_params(POST, AMEND_BORROWING_ORDER, params)

    def fix_loan_manual_reborrow(self, ordId=None, maxRate=None):
        params = {}
        if ordId is not None:
            params['ordId'] = ordId
        if maxRate is not None:
            params['maxRate'] = maxRate
        return self._request_with_params(POST, MANUAL_REBORROW, params)

    def repay_fix_loan_borrowing_order(self, ordId=None):
        params = {}
        if ordId is not None:
            params['ordId'] = ordId
        return self._request_with_params(POST, REPAY_BORROWING_ORDER, params)
    def get_fix_loan_borrowing_orders_list(self, ordId=None, ccy=None, state=None, after=None, before=None, limit=None):
        params = {}
        if ordId is not None:
            params['ordId'] = ordId
        if ccy is not None:
            params['ccy'] =ccy
        if state is not None:
            params['state'] = state
        if after is not None:
            params['after'] = after
        if before is not None:
            params['before'] = before
        if limit is not None:
            params['limit'] = limit
        return self._request_with_params(GET, BORROWING_ORDERS_LIST, params)

    def spot_manual_borrow_repay(self, ccy=None, side=None, amt=None):
        params = {}
        if ccy is not None:
            params['ccy'] = ccy
        if side is not None:
            params['side'] = side
        if amt is not None:
            params['amt'] = amt
        return self._request_with_params(POST, MANUAL_REBORROW_REPAY, params)

    def set_auto_repay(self, autoRepay=False):
        params = {}
        if autoRepay is not None:
            params['autoRepay'] = autoRepay
        return self._request_with_params(POST, SET_AUTO_REPAY, params)

    def spot_borrow_repay_history(self, ccy='', type='', after='', before='', limit=''):
        params = {'ccy': ccy, 'type': type, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, GET_BORROW_REPAY_HISTORY, params)
