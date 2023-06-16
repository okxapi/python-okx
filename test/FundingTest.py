
import unittest
from okx import Funding

class FundingTest(unittest.TestCase):
    def setUp(self):
        api_key = 'cfa1017d-940a-445f-af52-b340cbd6b0e0'
        api_secret_key = '6C50A4E980230A4BBE7046411DED0276'
        passphrase = '123456aA.'
        self.FundingAPI = Funding.FundingAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='0')
    """
    CANCEL_WITHDRAWAL = '/api/v5/asset/cancel-withdrawal' #need add
    CONVERT_DUST_ASSETS = '/api/v5/asset/convert-dust-assets' #need add
    ASSET_VALUATION = '/api/v5/asset/asset-valuation' #need add
    GET_SAVING_BALANCE = '/api/v5/asset/saving-balance' #need to add
    def test_asset_evluation(self):
        print(self.FundingAPI.get_asset_valuation("USDT"))
    def test_dust_convert_asset(self):
        print(self.FundingAPI.convert_dust_assets(["USDT"]))
    def test_saving_balance(self):
        print(self.FundingAPI.get_saving_balance())
    def test_asset_get_currency(self):
        print(self.FundingAPI.get_currency())
    def test_get_balance(self):
        print(self.FundingAPI.get_balances())
    def test_transfer(self):
        print(self.FundingAPI.funds_transfer("USDT","100","6","18"))
    def test_transfer_state(self):
        print(self.FundingAPI.transfer_state("11"))
    def test_get_bills(self):
        print(self.FundingAPI.get_bills())
    def test_deposit_lighting(self):
        print(self.FundingAPI.get_deposit_lightning("BTC","10"))
    def test_get_deposit_address(self):
        print(self.FundingAPI.get_deposit_address("BTC"))
    def test_get_deposit_history(self):
        print(self.FundingAPI.get_deposit_history())
    def test_withdraw(self):
        print(self.FundingAPI.coin_withdraw(ccy="USDT",amt = '10.0',dest = '3',toAddr="1391224291",fee="10"))
    def test_lighting_withdrawl(self):
        print(self.FundingAPI.withdrawal_lightning("BTC","jdsnjvhofhenogvne",memo="222"))
    def test_cancel_withdrawl(self):
        print(self.FundingAPI.cancel_withdrawal("sdhiadhsfdjknvjdaodns"))
    def test_get_withdrawal_history(self):
        print(self.FundingAPI.get_withdrawal_history())
    def test_purchase_redempt(self):
        print(self.FundingAPI.purchase_redempt("BTC",'1.0','purchase','0.1'))
    def test_set_lending_rate(self):
        print(self.FundingAPI.set_lending_rate("USDT","0.1"))
    def test_get_lending_history(self):
        print(self.FundingAPI.get_lending_history(ccy="USDT"))
    def test_get_lending_summary(self):
        print(self.FundingAPI.get_lending_rate_summary('BTC'))
    def test_get_lending_rate_history(self):
        print(self.FundingAPI.get_lending_rate_history())
        
    def test_get_lending_summary(self):
        print(self.FundingAPI.get_lending_rate_summary('BTC'))
    """

    # def test_get_lending_summary(self):
    #     print(self.FundingAPI.get_lending_rate_summary('BTC'))
    # def test_get_lending_rate_history(self):
    #     print(self.FundingAPI.get_lending_rate_history())

    # def test_get_non_tradable_assets(self):
    #     print(self.FundingAPI.get_non_tradable_assets())

    def test_get_deposit_withdraw_status(self):
        print(self.FundingAPI.get_deposit_withdraw_status(wdId='84804812'))

    # def test_get_withdrawal_history(self):
    #     print(self.FundingAPI.get_withdrawal_history())

    # def test_get_deposit_history(self):
    #     print(self.FundingAPI.get_deposit_history())

    # def test_withdrawal(self):
    #     print(self.FundingAPI.withdrawal(ccy='USDT',amt='1',dest='3',toAddr='18740405107',fee='0',areaCode='86'))

if __name__ == '__main__':
    unittest.main()