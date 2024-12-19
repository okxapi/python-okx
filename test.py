import okx.Earning as Earning
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class OKXSession:
    def __init__(self, apikey, secretkey, passphrase):
        self.flag = "0"
        self.eaningAPI = Earning.EarningAPI(apikey, secretkey, passphrase, flag=self.flag)

    def eth_product_info(self):
        result = self.eaningAPI.eth_product_info()
        print(result)

    def eth_purchase(self, amt):
        result = self.eaningAPI.eth_purchase(amt=amt)
        print(result)

    def eth_redeem(self, amt):
        result = self.eaningAPI.eth_redeem(amt=amt)
        print(result)

    def eth_balance(self):
        result = self.eaningAPI.eth_balance()
        print(result)

    def eth_purchase_redeem_history(self, type, status='', after='', before='', limit=''):
        result = self.eaningAPI.eth_purchase_redeem_history(type, status, after, before, limit)
        print(result)

    def eth_apy_history(self, days):
        result = self.eaningAPI.eth_apy_history(days=days)
        return result


if __name__ == '__main__':

    apikey, secretkey, passphrase = "", "", ""
    
    okx_session = OKXSession(apikey, secretkey, passphrase)
    # res = okx_session.eth_apy_history("365")
    # data = res.get('data')
    # df = pd.DataFrame(data)
    # df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    # df.to_excel('rates_data.xlsx', index=False)
    res = okx_session.eth_product_info()
    print(res)