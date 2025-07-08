import unittest
from okx import SubAccount

class SubAccountTest(unittest.TestCase):
    def setUp(self):
        api_key = 'your_apiKey'
        api_secret_key = 'your_secretKey'
        passphrase = 'your_secretKey'
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

    # def test_set_sub_accounts_VIP_loan(self):
    #     print(self.SubAccountApi.set_sub_accounts_VIP_loan(enable='true',alloc=[{'subAcct':'coretrading7',
    #                                                                              'loanAlloc':'1'}]))

    def test_get_sub_account_borrow_interest_and_limit(self):
        print(self.SubAccountApi.get_sub_account_borrow_interest_and_limit(subAcct='coretrading7'))

    # def test_get_history_of_managed_subAccount_transfer(self):
    #     print(self.SubAccountApi.get_history_of_managed_subAccount_transfer())

if __name__ == "__main__":
    unittest.main()