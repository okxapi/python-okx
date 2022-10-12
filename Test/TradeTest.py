import unittest
from ..okx import Trade
class TradeTest(unittest.TestCase):
    def setUp(self):
        api_key = '35d8f27e-63cc-45bc-a578-45d76363d47f'
        api_secret_key = '0B7C968025BC2D4D71CF74771EA0E15C'
        passphrase = '123456'
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
    def test_oneclick_repay_history(self):
        print(self.tradeApi.oneclick_repay_history())



if __name__=='__main__':
    unittest.main()
