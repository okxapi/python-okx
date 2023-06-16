from .client import Client
from .consts import *


class GridAPI(Client):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain = 'https://www.okx.com',debug = True):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain,debug)

    def grid_order_algo(self, instId='', algoOrdType='', maxPx='', minPx='', gridNum='', runType='', tpTriggerPx='',
                        slTriggerPx='', tag='', quoteSz='', baseSz='', sz='', direction='', lever='', basePos=''):
        params = {'instId': instId, 'algoOrdType': algoOrdType, 'maxPx': maxPx, 'minPx': minPx, 'gridNum': gridNum,
                  'runType': runType, 'tpTriggerPx': tpTriggerPx, 'slTriggerPx': slTriggerPx, 'tag': tag,
                  'quoteSz': quoteSz, 'baseSz': baseSz, 'sz': sz, 'direction': direction, 'lever': lever,
                  'basePos': basePos}
        return self._request_with_params(POST, GRID_ORDER_ALGO, params)

    def grid_amend_order_algo(self, algoId='', instId='', slTriggerPx='', tpTriggerPx=''):
        params = {'algoId': algoId, 'instId': instId, 'slTriggerPx': slTriggerPx, 'tpTriggerPx': tpTriggerPx}
        return self._request_with_params(POST, GRID_AMEND_ORDER_ALGO, params)

    def grid_stop_order_algo(self, algoId='', instId='', algoOrdType='', stopType=''):
        params = [{'algoId': algoId, 'instId': instId, 'algoOrdType': algoOrdType, 'stopType': stopType}]
        return self._request_with_params(POST, GRID_STOP_ORDER_ALGO, params)

    def grid_orders_algo_pending(self, algoOrdType='', algoId='', instId='', instType='', after='', before='',
                                 limit='', instFamily = ''):
        params = {'algoOrdType': algoOrdType, 'algoId': algoId, 'instId': instId, 'instType': instType, 'after': after,
                  'before': before, 'limit': limit,'instFamily':instFamily}
        return self._request_with_params(GET, GRID_ORDERS_ALGO_PENDING, params)

    def grid_orders_algo_history(self, algoOrdType='', algoId='', instId='', instType='', after='', before='',
                                 limit='',instFamily = ''):
        params = {'algoOrdType': algoOrdType, 'algoId': algoId, 'instId': instId, 'instType': instType, 'after': after,
                  'before': before, 'limit': limit,'instFamily':instFamily}
        return self._request_with_params(GET, GRID_ORDERS_ALGO_HISTORY, params)

    def grid_orders_algo_details(self, algoOrdType='', algoId=''):
        params = {'algoOrdType': algoOrdType, 'algoId': algoId}
        return self._request_with_params(GET, GRID_ORDERS_ALGO_DETAILS, params)

    def grid_sub_orders(self, algoId='', algoOrdType='', type='', groupId='', after='', before='', limit=''):
        params = {'algoId': algoId, 'algoOrdType': algoOrdType, 'type': type, 'groupId': groupId, 'after': after,
                  'before': before, 'limit': limit}
        return self._request_with_params(GET, GRID_SUB_ORDERS, params)

    def grid_positions(self, algoOrdType='', algoId=''):
        params = {'algoOrdType': algoOrdType, 'algoId': algoId}
        return self._request_with_params(GET, GRID_POSITIONS, params)

    def grid_withdraw_income(self, algoId=''):
        params = {'algoId': algoId}
        return self._request_with_params(POST, GRID_WITHDRAW_INCOME, params)

    def grid_compute_margin_balance(self, algoId='', type='', amt=''):
        params = {
            'algoId': algoId,
            'type': type,
            'amt': amt
        }
        return self._request_with_params(POST, GRID_COMPUTE_MARIGIN_BALANCE, params)

    def grid_adjust_margin_balance(self, algoId='', type='', amt='', percent=''):
        params = {
            'algoId': algoId,
            'type': type,
            'amt': amt,
            'percent': percent
        }
        return self._request_with_params(POST, GRID_MARGIN_BALANCE, params)

    def grid_ai_param(self, algoOrdType='', instId='', direction='', duration=''):
        params = {
            'algoOrdType': algoOrdType,
            'instId': instId,
            'direction': direction,
            'duration':duration
        }
        return self._request_with_params(GET, GRID_AI_PARAM, params)

    # - Place recurring buy order
    def place_recurring_buy_order(self, stgyName='', recurringList=[], period='', recurringDay='', recurringTime='',
                                  timeZone='', amt='', investmentCcy='', tdMode='', algoClOrdId='', tag=''):
        params = {'stgyName': stgyName, 'recurringList': recurringList, 'period': period, 'recurringDay': recurringDay,
                  'recurringTime': recurringTime,
                  'timeZone': timeZone, 'amt': amt, 'investmentCcy': investmentCcy, 'tdMode': tdMode,
                  'algoClOrdId': algoClOrdId, 'tag': tag}
        return self._request_with_params(POST, PLACE_RECURRING_BUY_ORDER, params)

    # - Amend recurring buy order
    def amend_recurring_buy_order(self, algoId='', stgyName=''):
        params = {'algoId': algoId, 'stgyName': stgyName}
        return self._request_with_params(POST, AMEND_RECURRING_BUY_ORDER, params)

    # - Stop recurring buy order
    def stop_recurring_buy_order(self, orders_data):
        return self._request_with_params(POST, STOP_RECURRING_BUY_ORDER, orders_data)

    # - Get recurring buy order list
    def get_recurring_buy_order_list(self, algoId='', after='', before='', limit=''):
        params = {
            'algoId': algoId,
            'after': after,
            'before': before,
            'limit': limit
        }
        return self._request_with_params(GET, GET_RECURRING_BUY_ORDER_LIST, params)

    # - Get recurring buy order history
    def get_recurring_buy_order_history(self, algoId='', after='', before='', limit=''):
        params = {
            'algoId': algoId,
            'after': after,
            'before': before,
            'limit': limit
        }
        return self._request_with_params(GET, GET_RECURRING_BUY_ORDER_HISTORY, params)

    # - Get recurring buy order details
    def get_recurring_buy_order_details(self, algoId=''):
        params = {'algoId': algoId}
        return self._request_with_params(GET, GET_RECURRING_BUY_ORDER_DETAILS, params)

    # - Get recurring buy sub orders
    def get_recurring_buy_sub_orders(self, algoId='', ordId='', after='', before='', limit=''):
        params = {
            'algoId': algoId,
            'ordId': ordId,
            'after': after,
            'before': before,
            'limit': limit
        }
        return self._request_with_params(GET, GET_RECURRING_BUY_SUB_ORDERS, params)
