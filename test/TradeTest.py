import unittest

from okx import Trade


class TradeTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
        self.tradeApi = Trade.TradeAPI(api_key, api_secret_key, passphrase, False, '1')

    # # """
    # def test_place_order(self):
    #     attachAlgoOrds = [{'tpTriggerPx': '49000.0', 'tpOrdPx': '-1', 'sz': '1', 'tpTriggerPxType': 'last'}];
    #     print(self.tradeApi.place_order(
    #         "BTC-USDT-SWAP", tdMode="isolated", clOrdId="asCai1234", side='buy', posSide="long", ordType="limit",
    #         sz="1",
    #         px="30000.0",
    #         attachAlgoOrds=attachAlgoOrds)
    #     );
    #
    #     attachAlgoOrds = [{'slTriggerPx': '25000.0', 'slOrdPx': '-1', 'sz': '1', 'slTriggerPxType': 'last'}];
    #     print(self.tradeApi.place_order(
    #         "BTC-USDT-SWAP", tdMode="isolated", clOrdId="asCai1234", side='buy', posSide="long", ordType="limit",
    #         sz="1",
    #         px="30000.0",
    #         attachAlgoOrds=attachAlgoOrds)
    #     );
    #
    #     attachAlgoOrds = [
    #         {
    #             "tpTriggerPxType": "last",
    #             "tpOrdPx": "-1",
    #             "tpTriggerPx": "34000",
    #             "sz": "1"
    #         },
    #         {
    #             "tpTriggerPxType": "last",
    #             "tpOrdPx": "-1",
    #             "tpTriggerPx": "35000",
    #             "sz": "1"
    #         },
    #         {
    #             "slTriggerPxType": "last",
    #             "slOrdPx": "-1",
    #             "slTriggerPx": "20000",
    #             "sz": "3"
    #         }
    #     ]
    #     print(self.tradeApi.place_order(
    #         "BTC-USDT-SWAP", tdMode="isolated", clOrdId="asCai1234", side='buy', posSide="long", ordType="limit",
    #         sz="1",
    #         px="30000.0",
    #         attachAlgoOrds=attachAlgoOrds)
    #     );

    # def test_cancel_order(self):
    #     print(self.tradeApi.cancel_order(instId="ETH-USDT",ordId="480702180748558336"))

    # def test_batch_order(self):
    #     orderData = [{
    #         "instId": "BTC-USDT-SWAP",
    #         "tdMode": "isolated",
    #         "clOrdId": "b15112122",
    #         "side": "buy",
    #         "posSide": "long",
    #         "ordType": "limit",
    #         "px": "30000.0",
    #         "sz": "2",
    #         "attachAlgoOrds": [{'tpTriggerPx': '50000.0', 'tpOrdPx': '-1', 'sz': '1', 'tpTriggerPxType': 'last'}]
    #     },
    #         {
    #             "instId": "BTC-USDT-SWAP",
    #             "tdMode": "isolated",
    #             "clOrdId": "b15112111",
    #             "side": "buy",
    #             "posSide": "long",
    #             "ordType": "limit",
    #             "px": "31000.0",
    #             "sz": "2",
    #             "attachAlgoOrds": [{'tpTriggerPx': '51000.0', 'tpOrdPx': '-1', 'sz': '1', 'tpTriggerPxType': 'last'}]
    #         }
    #     ]
    #
    #     print(self.tradeApi.place_multiple_orders(orderData))

    # 480702180748558336
    # def test_cancel_batch_orders(self):
    #     data=[
    #         {
    #             'instId':"ETH-USDT",
    #             'ordId':"480702885353881600"
    #         },
    #         {
    #             'instId':"BTC-USDT",
    #             'ordId':'480702885353881601'
    #         }
    #     ]
    #     print(self.tradeApi.cancel_multiple_orders(data))
    # def test_amend_order(self):
    #     attachAlgoOrds = [{'attachAlgoId': '672081789170569217', 'newTpTriggerPx': '55000.0'}];
    #     print(self.tradeApi.amend_order("BTC-USDT-SWAP", ordId="672081789170569216", newSz="1",
    #                                     attachAlgoOrds=attachAlgoOrds))

    # def test_amend_order_batch(self):
    #     orderData = [
    #         {
    #             'instId': 'BTC-USDT-SWAP',
    #             'ordId': '672081789170569216',
    #             'newSz': '1',
    #             "attachAlgoOrds": [{'attachAlgoId': '672081789170569217', 'newTpTriggerPx': '53000.0'}]
    #         }
    #     ]
    #
    #     print(self.tradeApi.amend_multiple_orders(orderData))

    # def test_close_all_positions(self):
    #     print(self.tradeApi.close_positions("BTC-USDT",mgnMode="cross"))
    # def test_get_order_info(self):
    #     print(self.tradeApi.get_orders("ETH-USDT","480707205436669952"))
    # def test_get_order_pending(self):
    #     print(self.tradeApi.get_order_list("SPOT"))
    # def test_get_order_history(self):
    #     print(self.tradeApi.get_orders_history("SPOT"))
    # def test_get_order_histry_archive(self):
    #     print(self.tradeApi.orders_history_archive("SPOT"))
    # def test_get_fills(self):
    #     print(self.tradeApi.get_fills(begin='1717045609000',end='1717045609100'))
    # def test_get_fills_history(self):
    #     print(self.tradeApi.get_fills_history("SPOT"))
    # def test_get_order_algo_pending(self):
    #     print(self.tradeApi.order_algos_list('oco'))
    # def test_order_algo(self):
    #     print(self.tradeApi.place_algo_order('BTC-USDT-SWAP', 'cross', side='buy', ordType='trigger', posSide='long',
    #                                      sz='100', triggerPx='22000', triggerPxType	='index', orderPx='-1'))
    # def test_cancel_algos(self):
    #     params = [{
    #     'algoId': '485903392536264704',
    #     'instId': 'BTC-USDT-SWAP'
    #     }]
    #
    #
    #     print(self.tradeApi.cancel_algo_order(params))
    #     def test_orders_algo_pending(self):
    #     print(self.tradeApi.order_algos_list(ordType='iceberg'))
    #     def test_algo_order_history(self):
    #     print(self.tradeApi.order_algos_history(algoId='485903392536264704',ordType='conditional'))
    #     def test_get_easy_convert_list(self):
    #     print(self.tradeApi.get_easy_convert_currency_list())
    #     def test_easy_convert(self):
    #     print(self.tradeApi.easy_convert(fromCcy=['BTC'],toCcy='OKB'))
    #     def test_get_convert_history(self):
    #     print(self.tradeApi.get_easy_convert_history())
    #     def test_get_oneclick_repay_support_list(self):
    #     print(self.tradeApi.get_oneclick_repay_list('cross'))
    #     def test_oneclick_repay(self):
    #     print(self.tradeApi.oneclick_repay(['BTC'],'USDT'))
    # 485903392536264704
    # 485936482235191296
    # def test_oneclick_repay_history(self):
    #     print(self.tradeApi.oneclick_repay_history())
    # def test_order_algo(self):
    #     print(self.tradeApi.place_algo_order(instId='BTC-USDT-SWAP', tdMode='cross', side='buy', ordType='conditional', \
    #         tpTriggerPx='15', tpOrdPx='18',sz='2'))

    # 581628185981308928
    # def test_get_algo_order_details(self):
    #     print(self.tradeApi.get_algo_order_details(algoId='581628185981308928'))

    # 581628185981308928
    # def test_amend_algo_order(self):
    #     print(self.tradeApi.amend_algo_order(instId='BTC-USDT-SWAP', algoId='581628185981308928',newSz='3'))

    # def test_get_order_history(self):
    #     print(self.tradeApi.get_orders_history(instType="SPOT",begin='1684857629313',end='1684857629313'))

    # def test_get_order_histry_archive(self):
    #     print(self.tradeApi.get_orders_history_archive(instType="SPOT",begin='1684857629313',end='1684857629313'))
    # def test_place_order(self):
    #     print(self.tradeApi.place_order("BTC-USDT", tdMode="cross", clOrdId="asCai1", side="buy", ordType="limit",
    #                                     sz="0.01", px="18000"))
    # def test_batch_order(self):
    #     orderData = [{
    #         "instId": "ETH-USDT",
    #         "tdMode": "cross",
    #         "clOrdId": "b151121",
    #         "side": "buy",
    #         "ordType": "limit",
    #         "px": "2.15",
    #         "sz": "2"
    #     },
    #         {
    #             "instId": "BTC-USDT",
    #             "tdMode": "cross",
    #             "clOrdId": "b152233",
    #             "side": "buy",
    #             "ordType": "limit",
    #             "px": "2.15",
    #             "sz": "2"
    #         }]
    #     print(self.tradeApi.place_multiple_orders(orderData))

    # 581616258865516544
    # 581616258865516545
    # def test_amend_order(self):
    #     print(self.tradeApi.amend_order("BTC-USDT", ordId="581616258865516544", newSz="0.03"))
    # def test_amend_order_batch(self):
    #     orderData = [
    #         {
    #             'instId': 'ETH-USDT',
    #             'ordId': '581616258865516544',
    #             'newSz': '0.02'
    #         },
    #         {
    #             'instId': 'BTC-USDT',
    #             'ordId': '581616258865516545',
    #             'newPx': '3.0'
    #         }
    #     ]
    #     print(self.tradeApi.amend_multiple_orders(orderData))

    # def test_order_algo(self):
    #
    #     print(self.tradeApi.place_algo_order(instId='BTC-USDT-SWAP', tdMode='cross', side='buy', ordType='conditional', \
    #                                          tpTriggerPx='15', tpOrdPx='18', sz='2',algoClOrdId='7678687',quickMgnType='manual'))

    # def test_order_algos_list(self):
    #     print(self.tradeApi.order_algos_list(ordType='conditional'))

    # def test_order_algo(self):
    #     print(self.tradeApi.place_order(instId='BTC-USDT-SWAP', tdMode='cross', side='buy',px='121',sz='2',
    #                                     clOrdId='234234565535',ordType='market'))
    # def test_close_all_positions(self):
    #     print(self.tradeApi.close_positions(instId="BTC-USDT-SWAP", mgnMode="cross",clOrdId='1213124'))

    def test_get_oneclick_repay_list_v2(self):
        print(self.tradeApi.get_oneclick_repay_list_v2())
    def test_oneclick_repay_v2(self):
        print(self.tradeApi.oneclick_repay_v2('BTC',['USDT']))
    def test_oneclick_repay_history_v2(self):
        print(self.tradeApi.oneclick_repay_history_v2())

if __name__ == '__main__':
    unittest.main()
