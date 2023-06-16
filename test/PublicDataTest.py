import unittest
from okx import PublicData
class publicDataTest(unittest.TestCase):
    def setUp(self):
        api_key = 'da097c9c-2f77-4dea-be18-2bfa77d0e394'
        api_secret_key = '56CC6C72D6B8A46EC993D48C83142A25'
        passphrase = '123456aA.'
        self.publicDataApi = PublicData.PublicAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')
    '''
    TestCase For:
    INTEREST_LOAN = '/api/v5/public/interest-rate-loan-quota' #need to add
    UNDERLYING = '/api/v5/public/underlying' #need to add
    VIP_INTEREST_RATE_LOAN_QUOTA = '/api/v5/public/vip-interest-rate-loan-quota' #need to add
    INSURANCE_FUND = '/api/v5/public/insurance-fund'#need to add
    CONVERT_CONTRACT_COIN = '/api/v5/public/convert-contract-coin' #need to add
    def test_interest_loan(self):
        print(self.publicDataApi.get_interest_rate_loan_quota())
    def test_get_underlying(self):
        print(self.publicDataApi.get_underlying("SWAP"))
    def test_get_vip_loan(self):
        print(self.publicDataApi.get_vip_interest_rate_loan_quota())
    def test_insurance_fund(self):
        print(self.publicDataApi.get_insurance_fund("SWAP",uly= "BTC-USD"))
    def test_convert_contract_coin(self):
        print(self.publicDataApi.get_convert_contract_coin(instId="BTC-USD-SWAP",sz = "1",px = "27000"))
    def test_get_instruments(self):
        print(self.publicDataApi.get_instruments("SPOT"))
    def test_delivery_exercise_history(self):
        print(self.publicDataApi.get_deliver_history("FUTURES","BTC-USD"))
    def test_get_open_interest(self):
        print(self.publicDataApi.get_open_interest("SWAP"))
    def test_get_funding_rate(self):
        print(self.publicDataApi.get_funding_rate("BTC-USD-SWAP"))
    def test_get_funding_rate_history(self):
        print(self.publicDataApi.funding_rate_history('BTC-USD-SWAP'))
    def test_get_price_limited(self):
        print(self.publicDataApi.get_price_limit("BTC-USD-SWAP"))
    def test_get_opt_summary(self):
        print(self.publicDataApi.get_opt_summary('BTC-USD'))

    def test_estimate_price(self):
        print(self.publicDataApi.get_estimated_price("BTC-USD-220831-17000-P"))
    def test_get_discount_rate_interest(self):
        print(self.publicDataApi.discount_interest_free_quota(ccy='ETH'))
    def test_get_systime(self):
        print(self.publicDataApi.get_system_time())
    def test_get_liquid_order(self):
        print(self.publicDataApi.get_liquidation_orders("SWAP",uly='BTC-USD',state='filled'))
    def test_get_mark_price(self):
        print(self.publicDataApi.get_mark_price('SWAP'))
    
    '''
    # def test_position_tier(self):
    #     print(self.publicDataApi.get_position_tiers('SWAP','cross',uly='ETH-USD'))

    # def test_get_option_tickBands(self):
    #     print(self.publicDataApi.get_option_tick_bands(instType='OPTION'))

    def test_get_option_trades(self):
        print(self.publicDataApi.get_option_trades(instFamily='BTC-USD'))

if __name__ == '__main__':
    unittest.main()