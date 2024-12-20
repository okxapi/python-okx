from okx import Earning, PublicData
from pandas import DataFrame

apikey = "YOUR_API_KEY"
secretkey = "YOUR_SECRET_KEY"
passphrase = "YOUR_PASSPHRASE"

flag = "0"

earningAPI = Earning.EarningAPI(apikey, secretkey, passphrase, False, flag)
publicDataAPI = PublicData.PublicAPI(flag=flag)

# Get beth apy history
result = earningAPI.get_apy_history("61")
data = result.get("data", [])
beth_apy_df = DataFrame(data)
print(beth_apy_df)

# Get funding rate history
data = []
result = publicDataAPI.funding_rate_history(
    instId="ETH-USDT-SWAP",
    before="1724544000000"
)
tmp = result.get("data", [])
if len(tmp) == 100:
    data += tmp
    while len(tmp) == 100:
        result = publicDataAPI.funding_rate_history(
            instId="ETH-USDT-SWAP",
            before=tmp[0].get("fundingTime")
        )
        tmp = result.get("data", [])
        data += tmp
funding_rate_df = DataFrame(data)
print(funding_rate_df)

