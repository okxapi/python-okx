from .client import Client
from .consts import *


class TradeAPI(Client):

    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=False, flag='1', domain = 'https://www.okx.com',debug = True):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain,debug)

    # Place Order
    def place_order(self, instId, tdMode, side, ordType, sz, ccy='', clOrdId='', tag='', posSide='', px='',
                    reduceOnly='', tgtCcy='', tpTriggerPx='', tpOrdPx='', slTriggerPx='', slOrdPx='',
                    tpTriggerPxType='', slTriggerPxType='', quickMgnType='', stpId='', stpMode=''):
        params = {'instId': instId, 'tdMode': tdMode, 'side': side, 'ordType': ordType, 'sz': sz, 'ccy': ccy,
                  'clOrdId': clOrdId, 'tag': tag, 'posSide': posSide, 'px': px, 'reduceOnly': reduceOnly,
                  'tgtCcy': tgtCcy, 'tpTriggerPx': tpTriggerPx, 'tpOrdPx': tpOrdPx, 'slTriggerPx': slTriggerPx,
                  'slOrdPx': slOrdPx, 'tpTriggerPxType': tpTriggerPxType, 'slTriggerPxType': slTriggerPxType,
                  'quickMgnType': quickMgnType, 'stpId': stpId, 'stpMode': stpMode}
        return self._request_with_params(POST, PLACR_ORDER, params)

    # Place Multiple Orders
    def place_multiple_orders(self, orders_data):
        return self._request_with_params(POST, BATCH_ORDERS, orders_data)

    # Cancel Order
    def cancel_order(self, instId, ordId='', clOrdId=''):
        params = {'instId': instId, 'ordId': ordId, 'clOrdId': clOrdId}
        return self._request_with_params(POST, CANAEL_ORDER, params)

    # Cancel Multiple Orders
    def cancel_multiple_orders(self, orders_data):
        return self._request_with_params(POST, CANAEL_BATCH_ORDERS, orders_data)

    # Amend Order
    def amend_order(self, instId, cxlOnFail='', ordId='', clOrdId='', reqId='', newSz='', newPx='', newTpTriggerPx='',
                    newTpOrdPx='', newSlTriggerPx='', newSlOrdPx='', newTpTriggerPxType='', newSlTriggerPxType=''):
        params = {'instId': instId, 'cxlOnFailc': cxlOnFail, 'ordId': ordId, 'clOrdId': clOrdId, 'reqId': reqId,
                  'newSz': newSz, 'newPx': newPx, 'newTpTriggerPx': newTpTriggerPx, 'newTpOrdPx': newTpOrdPx,
                  'newSlTriggerPx': newSlTriggerPx, 'newSlOrdPx': newSlOrdPx, 'newTpTriggerPxType': newTpTriggerPxType,
                  'newSlTriggerPxType': newSlTriggerPxType}
        return self._request_with_params(POST, AMEND_ORDER, params)

    # Amend Multiple Orders
    def amend_multiple_orders(self, orders_data):
        return self._request_with_params(POST, AMEND_BATCH_ORDER, orders_data)

    # Close Positions
    def close_positions(self, instId, mgnMode, posSide='', ccy='', autoCxl='', clOrdId='', tag=''):
        params = {'instId': instId, 'mgnMode': mgnMode, 'posSide': posSide, 'ccy': ccy, 'autoCxl': autoCxl,
                  'clOrdId': clOrdId, 'tag': tag}
        return self._request_with_params(POST, CLOSE_POSITION, params)

    # Get Order Details
    def get_order(self, instId, ordId='', clOrdId=''):
        params = {'instId': instId, 'ordId': ordId, 'clOrdId': clOrdId}
        return self._request_with_params(GET, ORDER_INFO, params)

    # Get Order List
    def get_order_list(self, instType='', uly='', instId='', ordType='', state='', after='', before='', limit='',instFamily = ''):
        params = {'instType': instType, 'uly': uly, 'instId': instId, 'ordType': ordType, 'state': state,
                  'after': after, 'before': before, 'limit': limit,'instFamily':instFamily}
        return self._request_with_params(GET, ORDERS_PENDING, params)

    # Get Order History (last 7 days）
    def get_orders_history(self, instType, uly='', instId='', ordType='', state='', after='', before='', begin='',
                           end='', limit='', instFamily=''):
        params = {'instType': instType, 'uly': uly, 'instId': instId, 'ordType': ordType, 'state': state,
                  'after': after, 'before': before, 'begin': begin, 'end': end, 'limit': limit,
                  'instFamily': instFamily}
        return self._request_with_params(GET, ORDERS_HISTORY, params)

    # Get Order History (last 3 months)
    def get_orders_history_archive(self, instType, uly='', instId='', ordType='', state='', after='', before='',
                                   begin='', end='', limit='', instFamily=''):
        params = {'instType': instType, 'uly': uly, 'instId': instId, 'ordType': ordType, 'state': state,
                  'after': after, 'before': before, 'begin': begin, 'end': end, 'limit': limit,
                  'instFamily': instFamily}
        return self._request_with_params(GET, ORDERS_HISTORY_ARCHIVE, params)

    # Get Transaction Details
    def get_fills(self, instType='', uly='', instId='', ordId='', after='', before='', limit='',instFamily = ''):
        params = {'instType': instType, 'uly': uly, 'instId': instId, 'ordId': ordId, 'after': after, 'before': before,
                  'limit': limit,'instFamily':instFamily}
        return self._request_with_params(GET, ORDER_FILLS, params)

    # Place Algo Order
    def place_algo_order(self, instId='', tdMode='', side='', ordType='', sz='', ccy='',
                         posSide='', reduceOnly='', tpTriggerPx='',
                         tpOrdPx='', slTriggerPx='', slOrdPx='',
                         triggerPx='', orderPx='', tgtCcy='', pxVar='',
                         pxSpread='',
                         szLimit='', pxLimit='', timeInterval='', tpTriggerPxType='', slTriggerPxType='',
                         callbackRatio='',callbackSpread='',activePx='',tag='',triggerPxType='',closeFraction=''
                         ,quickMgnType='',algoClOrdId=''):
        params = {'instId': instId, 'tdMode': tdMode, 'side': side, 'ordType': ordType, 'sz': sz, 'ccy': ccy,
                  'posSide': posSide, 'reduceOnly': reduceOnly, 'tpTriggerPx': tpTriggerPx, 'tpOrdPx': tpOrdPx,
                  'slTriggerPx': slTriggerPx, 'slOrdPx': slOrdPx, 'triggerPx': triggerPx, 'orderPx': orderPx,
                  'tgtCcy': tgtCcy, 'pxVar': pxVar, 'szLimit': szLimit, 'pxLimit': pxLimit,
                  'timeInterval': timeInterval,
                  'pxSpread': pxSpread, 'tpTriggerPxType': tpTriggerPxType, 'slTriggerPxType': slTriggerPxType,
                  'callbackRatio' : callbackRatio, 'callbackSpread':callbackSpread,'activePx':activePx,
                  'tag':tag,'triggerPxType':triggerPxType,'closeFraction':closeFraction,'quickMgnType':quickMgnType,'algoClOrdId':algoClOrdId}
        return self._request_with_params(POST, PLACE_ALGO_ORDER, params)

    # Cancel Algo Order
    def cancel_algo_order(self, params):
        return self._request_with_params(POST, CANCEL_ALGOS, params)

    # Cancel Advance Algos
    def cancel_advance_algos(self,params):
        return self._request_with_params(POST, Cancel_Advance_Algos, params)

    # Get Algo Order List
    def order_algos_list(self, ordType='', algoId='', instType='', instId='', after='', before='', limit='',algoClOrdId=''):
        params = {'ordType': ordType, 'algoId': algoId, 'instType': instType, 'instId': instId, 'after': after,
                  'before': before, 'limit': limit, 'algoClOrdId': algoClOrdId}
        return self._request_with_params(GET, ORDERS_ALGO_OENDING, params)

    # Get Algo Order History
    def order_algos_history(self, ordType, state='', algoId='', instType='', instId='', after='', before='', limit=''):
        params = {'ordType': ordType, 'state': state, 'algoId': algoId, 'instType': instType, 'instId': instId,
                  'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, ORDERS_ALGO_HISTORY, params)

    # Get Transaction Details History
    def get_fills_history(self, instType, uly='', instId='', ordId='', after='', before='', limit='',instFamily=''):
        params = {'instType': instType, 'uly': uly, 'instId': instId, 'ordId': ordId, 'after': after, 'before': before,
                  'limit': limit,'instFamily':instFamily}
        return self._request_with_params(GET, ORDERS_FILLS_HISTORY, params)

    def get_easy_convert_currency_list(self):
        return self._request_without_params(GET, EASY_CONVERT_CURRENCY_LIST)

    def easy_convert(self,fromCcy = [],toCcy = ''):
        params = {
            'fromCcy':fromCcy,
            'toCcy':toCcy
        }
        return self._request_with_params(POST, EASY_CONVERT, params)

    def get_easy_convert_history(self,before = '',after = '',limit = ''):
        params = {
            'before':before,
            'after':after,
            'limit':limit
        }
        return self._request_with_params(GET,CONVERT_EASY_HISTORY,params)

    def get_oneclick_repay_list(self,debtType = ''):
        params = {
            'debtType':debtType
        }
        return self._request_with_params(GET,ONE_CLICK_REPAY_SUPPORT,params)

    def oneclick_repay(self,debtCcy = [] , repayCcy=''):
        params = {
            'debtCcy':debtCcy,
            'repayCcy':repayCcy
        }
        return self._request_with_params(POST,ONE_CLICK_REPAY,params)

    def oneclick_repay_history(self,after = '',before = '',limit = ''):
        params = {
            'after':after,
            'before':before,
            'limit':limit
        }
        return self._request_with_params(GET,ONE_CLICK_REPAY_HISTORY,params)

    # Get algo order details
    def get_algo_order_details(self, algoId='', algoClOrdId=''):
        params = {'algoId': algoId, 'algoClOrdId': algoClOrdId}
        return self._request_with_params(GET, GET_ALGO_ORDER_DETAILS, params)

    # Amend algo order
    def amend_algo_order(self, instId='', algoId='', algoClOrdId='', cxlOnFail='', reqId='', newSz='',
                         newTpTriggerPx='', newTpOrdPx='', newSlTriggerPx='', newSlOrdPx='', newTpTriggerPxType='',
                         newSlTriggerPxType=''):
        params = {'instId': instId, 'algoId': algoId, 'algoClOrdId': algoClOrdId, 'cxlOnFail': cxlOnFail,
                  'reqId': reqId, 'newSz': newSz, 'newTpTriggerPx': newTpTriggerPx, 'newTpOrdPx': newTpOrdPx,
                  'newSlTriggerPx': newSlTriggerPx, 'newSlOrdPx': newSlOrdPx,
                  'newTpTriggerPxType': newTpTriggerPxType, 'newSlTriggerPxType': newSlTriggerPxType}
        return self._request_with_params(POST, AMEND_ALGO_ORDER, params)
