import unittest

from loguru import logger

from okx import Account, SimpleEarnFixed


class SimpleEarnFixedTest(unittest.TestCase):
    def setUp(self):
        api_key = '15c0a341-f38c-4bf2-8f86-3c32c8b5d60c'
        api_secret_key = 'DEBF51E2733E03CE4F2CEB63BB01D983'
        passphrase = 'hylHYL950525,.'
        self.SimpleEarnFixedAPI = SimpleEarnFixed.SimpleEarnFixedAPI(api_key, api_secret_key, passphrase, flag='1')

    # def test_get_lending_offers(self):
    #     logger.debug(self.SimpleEarnFixedAPI.get_lending_offers())
    #
    # def test_get_instruments(self):
    #     logger.debug(self.SimpleEarnFixedAPI.get_lending_apy_history(ccy="BTC", term='30D'))
    #
    # def test_get_pending_lending_volume(self):
    #     logger.debug(self.SimpleEarnFixedAPI.get_pending_lending_volume(ccy="BTC", term='30D'))
    #
    # def test_place_lending_order(self):
    #     logger.debug(self.SimpleEarnFixedAPI.place_lending_order(ccy="USDT", amt="33", maxRate="1", term="30D"))
    #
    # def test_amend_lending_order(self):
    #     logger.debug(self.SimpleEarnFixedAPI.amend_lending_order(ordId="2407241551594080",changeAmt="30",autoRenewal=True))
    #
    # def test_get_lending_orders_list(self):
    #     logger.debug(self.SimpleEarnFixedAPI.get_lending_orders_list())
    # def test_get_lending_sub_orders(self):
    #     logger.debug(self.SimpleEarnFixedAPI.get_lending_sub_orders(ordId="2407241453209933"))


if __name__ == '__main__':
    unittest.main()