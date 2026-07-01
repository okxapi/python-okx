from okx.okxclient import OkxClient
from okx.consts import *


class EarnAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1', domain='https://www.okx.com', debug=False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    # Cancel a pending staking redemption — POST /api/v5/earn/staking-cancel-redeem
    def staking_cancel_redeem(self, ordId=''):
        params = {
            'ordId': ordId,
        }
        return self._request_with_params(POST, STAKING_CANCEL_REDEEM, params)

    # Get on-chain staking products — GET /api/v5/earn/staking-products
    def get_staking_products(self, ccy='', productId=''):
        params = {}
        if ccy != '':
            params['ccy'] = ccy
        if productId != '':
            params['productId'] = productId
        return self._request_with_params(GET, STAKING_PRODUCTS, params)
