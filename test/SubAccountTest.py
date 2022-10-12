import unittest
from ..okx import SubAccount

class SubAccountTest(unittest.TestCase):
    def setUp(self):
        api_key = '52c37310-a8b0-454a-8191-3250acff2626'
        api_secret_key = 'EC37534156E6B8C32E78FE8D8C1D506B'
        passphrase = 'Hanhao0.0'
        self.SubAccountApi = SubAccount.SubAccountAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')
    '''
    ENTRUST_SUBACCOUNT_LIST = '/api/v5/users/entrust-subaccount-list' #need to add
    SET_TRSNSFER_OUT = '/api/v5/users/subaccount/set-transfer-out' #need to add
    GET_ASSET_SUBACCOUNT_BALANCE = '/api/v5/asset/subaccount/balances' #need to add
    
    def test_set_permission_transfer_out(self):
        print(self.SubAccountApi.set_permission_transfer_out("tst123qwerq", "false"))
    def test_entrust_subaccount_list(self):
        print(self.SubAccountApi.get_entrust_subaccount_list())

    def test_subaccount_funding_balance(self):
        print(self.SubAccountApi.subaccount_funding_balance("unitTest1298"))
        
    def test_get_subaccount_list(self):
        print(self.SubAccountApi.view_list())
    def test_modified_apiKey(self):
        print(self.SubAccountApi.reset(''))
    def test_get_subaccount_balance(self):
        #zsynoaff02
        print(self.SubAccountApi.balances('zsynoaff02'))
    def test_get_subaccount_bills(self):
        print(self.SubAccountApi.bills())
    def test_subaccount_transfer(self):
        print(self.SubAccountApi.subAccount_transfer())
    def test_subaccount_transfer(self):
        print(self.SubAccountApi.subAccount_transfer(ccy = 'BTC', amt = '1.0', froms= '18', to='18', fromSubAccount='zsynoaff02',toSubAccount = 'unitTest1298'))

    '''

if __name__ == "__main__":
    unittest.main()