import unittest
from okx import Status

class StackingTest(unittest.TestCase):
    def setUp(self):
        api_key = 'ef06bf27-6a01-4797-b801-e3897031e45d'
        api_secret_key = 'D3620B2660203350EEE80FDF5BE0C960'
        passphrase = 'Beijing123'
        self.StackingAPI = Status.StackingAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')
    '''
    STACK_DEFI_OFFERS = '/api/v5/finance/staking-defi/offers'
    STACK_DEFI_PURCHASE = '/api/v5/finance/staking-defi/purchase'
    STACK_DEFI_REDEEM = '/api/v5/finance/staking-defi/redeem'
    STACK_DEFI_CANCEL = '/api/v5/finance/staking-defi/cancel'
    STACK_DEFI_ORDERS_ACTIVITY = '/api/v5/finance/staking-defi/orders-active'
    STACK_DEFI_ORDERS_HISTORY = '/api/v5/finance/staking-defi/orders-history'
    '''
    def test_get_offers(self):
        print(self.StackingAPI.get_offers(ccy="USDT"))

    
    
    def test_purcase(self):
        print(self.StackingAPI.purchase(1456,"USDT","100","0"))

if __name__ == "__main__":
    unittest.main()