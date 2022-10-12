
import unittest
from ..okx import NDBroker

class BrokerTest(unittest.TestCase):
    def setUp(self):
        '''

        52c37310-a8b0-454a-8191-3250acff2626
        EC37534156E6B8C32E78FE8D8C1D506B
        Hanhao0.0
        '''
        api_key = '52c37310-a8b0-454a-8191-3250acff2626'
        api_secret_key = 'EC37534156E6B8C32E78FE8D8C1D506B'
        passphrase = 'Hanhao0.0'
        self.NDBrokerAPI = NDBroker.NDBrokerAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')

    '''
    def test_get_broker_info(self):
        result = self.NDBrokerAPI.get_broker_info()
        print(result)
    
    def test_create_subAccount(self):
        print(self.NDBrokerAPI.create_subaccount("",""))
        #{'code': '0', 'data': [{'acctLv': '1', 'label': 'unitTest', 'subAcct': 'unitTest1298', 'ts': '1660789737257', 'uid': '346146586377719875'}], 'msg': ''}
    

    
    def test_get_subaccount_info(self):
        print(self.NDBrokerAPI.get_subaccount_info())
    
    def test_subaccount_create_apikey(self):
        print(self.NDBrokerAPI.create_subaccount_apikey("unitTest1298",'test2222',"114514A.bc","142.112.128.63","trade"))
        #{'code': '0', 'data': [{'apiKey': 'faf24bd1-dc25-45ab-9f78-ebfea58614bd', 'ip': '142.112.128.63', 'label': 'test2222', 'passphrase': '114514A.bc', 'perm': 'read_only,trade', 'secretKey': 'DB4F607380AA04313BB0DEDBFE576FF1', 'subAcct': 'unitTest1298', 'ts': '1660793476848'}], 'msg': ''}
    
    def test_subaccount_get_apikey(self):
        print(self.NDBrokerAPI.get_subaccount_apikey("unitTest1298","faf24bd1-dc25-45ab-9f78-ebfea58614bd"))
    
    def test_delete_subAccount(self):
        print(self.NDBrokerAPI.delete_subaccount("hanhaoBras1234"))


    def test_modifiy_subaccount_apikey(self):
        print(self.NDBrokerAPI.reset_subaccount_apikey("unitTest1298","faf24bd1-dc25-45ab-9f78-ebfea58614bd","csuihssssiani",perm="trade",ip = "192.168.1.1"))

    def test_delete_subaccount_apikey(self):
        print(self.NDBrokerAPI.delete_subaccount_apikey("unitTest1298","faf24bd1-dc25-45ab-9f78-ebfea58614bd"))
        
    def test_set_account_lv(self):
        print(self.NDBrokerAPI.set_subaccount_level("unitTest1298","4"))
    
    def test_delete_subaccount_apikey(self):
        print(self.NDBrokerAPI.delete_subaccount_apikey("unitTest1298","faf24bd1-dc25-45ab-9f78-ebfea58614bd"))
    
    def test_set_fee_rate(self):
        print(self.NDBrokerAPI.set_subaccount_fee_rate("unitTest1298","SPOT","absolute","90","90"))
    def test_create_desposit(self):
        print(self.NDBrokerAPI.create_subaccount_deposit_address("unitTest1298","ETH"))
    def test_rebate_daily(self):
        print(self.NDBrokerAPI.get_rebate_daily())
    


    def test_create_rebate_per_order(self):
        print(self.NDBrokerAPI.generate_rebate_per_orders("20220501","20220801"))
    '''
    def test_get_rebate_per_order(self):
        print(self.NDBrokerAPI.get_rebate_per_orders("false",begin="20220501",end = "20220801"))
if __name__ == '__main__':
  unittest.main()