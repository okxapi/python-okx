import unittest
from okx import Trade
class TradeTest(unittest.TestCase):
    def setUp(self):
        api_key = 'da097c9c-2f77-4dea-be18-2bfa77d0e394'
        api_secret_key = '56CC6C72D6B8A46EC993D48C83142A25'
        passphrase = '123456aA.'
        self.tradeApi = Trade.TradeAPI(api_key, api_secret_key, passphrase, False, '1')
    """
    def test_place_order(self):
        print(self.tradeApi.place_order("BTC-USDT",tdMode="cross",clOrdId="asCai1",side="buy",ordType="limit",sz="0.01",px="18000"))
    def test_cancel_order(self):
        print(self.tradeApi.cancel_order(instId="ETH-USDT",ordId="480702180748558336"))

    def test_batch_order(self):
        orderData = [    {
        "instId":"ETH-USDT",
        "tdMode":"cross",
        "clOrdId":"b151121",
        "side":"buy",
        "ordType":"limit",
        "px":"2.15",
        "sz":"2"
    },
    {
        "instId":"BTC-USDT",
        "tdMode":"cross",
        "clOrdId":"b152233",
        "side":"buy",
        "ordType":"limit",
        "px":"2.15",
        "sz":"2"
    }]
        print(self.tradeApi.place_multiple_orders(orderData))
    #480702180748558336
    def test_cancel_batch_orders(self):
        data=[
            {
                'instId':"ETH-USDT",
                'ordId':"480702885353881600"
            },
            {
                'instId':"BTC-USDT",
                'ordId':'480702885353881601'
            }
        ]
        print(self.tradeApi.cancel_multiple_orders(data))
    def test_amend_order(self):
        print(self.tradeApi.amend_order("BTC-USDT",ordId="480706017781743616",newSz="0.03"))
    def test_amend_order_batch(self):
        orderData = [
            {
                'instId':'ETH-USDT',
                'ordId':'480707205436669952',
                'newSz':'0.02'
            },
            {
                'instId':'BTC-USDT',
                'ordId':'480707205436669953',
                'newPx':'3.0'
            }
        ]
        print(self.tradeApi.amend_multiple_orders(orderData))
    def test_close_all_positions(self):
        print(self.tradeApi.close_positions("BTC-USDT",mgnMode="cross"))
    def test_get_order_info(self):
        print(self.tradeApi.get_orders("ETH-USDT","480707205436669952"))
    def test_get_order_pending(self):
        print(self.tradeApi.get_order_list("SPOT"))
    def test_get_order_history(self):
        print(self.tradeApi.get_orders_history("SPOT"))
    def test_get_order_histry_archive(self):
        print(self.tradeApi.orders_history_archive("SPOT"))
    def test_get_fills(self):
        print(self.tradeApi.get_fills("SPOT"))
    def test_get_fills_history(self):
        print(self.tradeApi.get_fills_history("SPOT"))
    def test_get_order_algo_pending(self):
        print(self.tradeApi.order_algos_list('oco'))
    def test_order_algo(self):
        print(self.tradeApi.place_algo_order('BTC-USDT-SWAP', 'cross', side='buy', ordType='trigger', posSide='long',
                                         sz='100', triggerPx='22000', triggerPxType	='index', orderPx='-1'))
    def test_cancel_algos(self):
        params = [{
        'algoId': '485903392536264704',
        'instId': 'BTC-USDT-SWAP'
        }]


        print(self.tradeApi.cancel_algo_order(params))
        def test_cancel_adv_algos(self):
        params = [{
            'algoId': '485936482235191296',
            'instId': 'BTC-USDT-SWAP'
        }]

        print(self.tradeApi.cancel_advance_algos(params)))
        def test_orders_algo_pending(self):
        print(self.tradeApi.order_algos_list(ordType='iceberg'))
        def test_algo_order_history(self):
        print(self.tradeApi.order_algos_history(algoId='485903392536264704',ordType='conditional'))
        def test_get_easy_convert_list(self):
        print(self.tradeApi.get_easy_convert_currency_list())
        def test_easy_convert(self):
        print(self.tradeApi.easy_convert(fromCcy=['BTC'],toCcy='OKB'))
        def test_get_convert_history(self):
        print(self.tradeApi.get_easy_convert_history())
        def test_get_oneclick_repay_support_list(self):
        print(self.tradeApi.get_oneclick_repay_list('cross'))
        def test_oneclick_repay(self):
        print(self.tradeApi.oneclick_repay(['BTC'],'USDT'))
"""
#485903392536264704
    #485936482235191296
    # def test_oneclick_repay_history(self):
    #     print(self.tradeApi.oneclick_repay_history())
    # def test_order_algo(self):
    #     print(self.tradeApi.place_algo_order(instId='BTC-USDT-SWAP', tdMode='cross', side='buy', ordType='conditional', \
    #         tpTriggerPx='15', tpOrdPx='18',sz='2'))

    # 581628185981308928
    # def test_get_algo_order_details(self):
    #     print(self.tradeApi.get_algo_order_details(algoId='581628185981308928'))

    #581628185981308928
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

        #581616258865516544
        #581616258865516545
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

    def test_order_algos_list(self):
        print(self.tradeApi.order_algos_list(ordType='conditional'))

    # def test_order_algo(self):
    #     print(self.tradeApi.place_order(instId='BTC-USDT-SWAP', tdMode='cross', side='buy',px='121',sz='2',
    #                                     clOrdId='234234565535',ordType='market'))
    # def test_close_all_positions(self):
    #     print(self.tradeApi.close_positions(instId="BTC-USDT-SWAP", mgnMode="cross",clOrdId='1213124'))
if __name__=='__main__':
    unittest.main()
