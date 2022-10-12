import json
import time

import okx.Account as Account


async def http2_request(request, parameters):
    while 1:
        begin = time.time()
        if type(parameters) is list:
            result = request(*parameters)
        else:
            result = request(**parameters)

        end = time.time()
        cost = end - begin
        print(f'request_cost:{cost}\nresponse_body:{json.dumps(result)}')


api_key = ""
secret_key = ""
passphrase = ""
# flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
# flag = '1'  # 模拟盘 demo trading
flag = '0'  # 实盘 real tradiang

if __name__ == '__main__':
    # account api
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
    accountAPI.get_account_config()
    accountAPI.get_greeks('BTC')
