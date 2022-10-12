
import unittest
from ..okx import Grid

class GridTest(unittest.TestCase):
    def setUp(self):
        api_key = 'ef06bf27-6a01-4797-b801-e3897031e45d'
        api_secret_key = 'D3620B2660203350EEE80FDF5BE0C960'
        passphrase = 'Beijing123'
        self.GridAPI = Grid.GridAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1', debug=False)
    """
    GRID_COMPUTE_MARIGIN_BALANCE = '/api/v5/tradingBot/grid/compute-margin-balance'
    GRID_MARGIN_BALANCE = '/api/v5/tradingBot/grid/margin-balance'
    GRID_AI_PARAM = '/api/v5/tradingBot/grid/ai-param'
    
    def test_ai_param(self):
        print(self.GridAPI.grid_ai_param("grid","BTC-USDT"))

    def test_order_algo(self):
        print(self.GridAPI.grid_order_algo("BTC-USDT","grid","45000","20000","100","1",quoteSz="50"))
    #479973849967362048
    def test_grid_margin_balance(self):
        print(self.GridAPI.grid_adjust_margin_balance())
    def test_compute_margin_balance(self):
        print(self.GridAPI.grid_compute_margin_balance("479978879210491904","add","100"))

    def test_pending_grid_order(self):
        print(self.GridAPI.grid_orders_algo_pending("grid"))
    def test_amend_order_algo(self):
        print(self.GridAPI.grid_amend_order_algo('485238792325173248','BTC-USDT-SWAP',tpTriggerPx='50000'))
    def test_stop_order_algo(self):
        print(self.GridAPI.grid_stop_order_algo('485238792325173248','BTC-USDT-SWAP','contract_grid','1'))
    def test_pending_grid_order(self):
        print(self.GridAPI.grid_orders_algo_pending("grid"))
    def test_algo_history(self):
        print(self.GridAPI.grid_orders_algo_history('contract_grid'))
    def test_orders_algo_details(self):
        print(self.GridAPI.grid_orders_algo_details('contract_grid','485238792325173248'))
    def test_get_sub_orders(self):
        print(self.GridAPI.grid_sub_orders('485238792325173248','contract_grid','filled'))
    def test_order_algo2(self):
        print(self.GridAPI.grid_order_algo("BTC-USDT-SWAP","contract_grid","45000","20000","100","1",sz='3000',direction='long',lever='3.0'))
    def test_get_positions(self):
        print(self.GridAPI.grid_positions('contract_grid','485379848832286720'))
    def test_withdrawl_profits(self):
        print(self.GridAPI.grid_withdraw_income('11111'))
    def test_withdrawl_profits(self):
        print(self.GridAPI.grid_withdraw_income('485380442313723904'))
    """


    def test_order_algo(self):
        print(self.GridAPI.grid_order_algo("BTC-USDT","grid","45000","20000","100","1",quoteSz="50"))
if __name__ == '__main__':
    unittest.main()