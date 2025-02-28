import unittest

from loguru import logger

from okx import Account


class AccountTest(unittest.TestCase):
    def setUp(self):
        api_key = '52049394-3c72-4c06-8d87-d6399450c264'
        api_secret_key = 'E532EB5AF81E6E50A2875225FEDC9150'
        passphrase = 'Fixedloan2024!'
        self.AccountAPI = Account.AccountAPI(api_key, api_secret_key, passphrase, flag='1')

    # '''
    # POSITIONS_HISTORY = '/api/v5/account/positions-history' #need add
    # GET_PM_LIMIT = '/api/v5/account/position-tiers' #need add
    # ACCOUNT_RISK = '/api/v5/account/risk-state' #need add
    # def test_account_risk(self):
    #     print(self.AccountAPI.get_account_risk())
    #
    # def test_get_pm_limit(self):
    #     print(self.AccountAPI.get_pm_limit("SWAP","BTC-USDT"))
    # positions-history
    # def test_get_positions_history(self):
    #     print(self.AccountAPI.get_positions_history())
    # def test_get_instruments(self):
    #     print(self.AccountAPI.get_instruments(instType='SPOT'))
    # def test_get_account_bills_archive(self):
    #     print(self.AccountAPI.get_account_bills_archive(begin='1715780962300',end='1716998400000'))
    # def test_positions_builder(self):
    #     print("Both real and virtual positions and assets are calculated")
    #     sim_pos = [{'instId': 'BTC-USDT-SWAP', 'pos': '10'}, {'instId': 'BTC-USDT-SWAP', 'pos': '10'}]
    #     sim_asset = [{'ccy': 'USDT', 'amt': '100'}]
    #     print(self.AccountAPI.position_builder(inclRealPosAndEq=False, spotOffsetType='1', greeksType='CASH',
    #                                            simPos=sim_pos, simAsset=sim_asset))
    #
    #     print("Only existing real positions are calculated")
    #     print(self.AccountAPI.position_builder(inclRealPosAndEq=True, greeksType='CASH'))
    #
    #     print("Only virtual positions are calculated")
    #     print(self.AccountAPI.position_builder(inclRealPosAndEq=False, simPos=sim_pos))

    # def test_get_user_config(self):
    #     print(self.AccountAPI.get_account_config())
    # def test_get_positions(self):
    #     print(self.AccountAPI.get_positions("SWAP"))
    # def test_get_balance(self):
    #     print(self.AccountAPI.get_account())
    # def test_get_positions_risk(self):
    #     print(self.AccountAPI.get_position_risk("SWAP"))
    # def test_get_bills(self):
    #     print(self.AccountAPI.get_bills_detail())
    #
    # def test_get_bills_arch(self):
    #     print(self.AccountAPI.get_bills_details())
    # def test_set_position_mode(self):
    #     print(self.AccountAPI.set_position_mode("long_short_mode"))
    # def test_set_leverage(self):
    #     print(self.AccountAPI.set_leverage(instId="BTC-USDT",lever="5",mgnMode="isolated"))
    # def test_get_max_avaliable_size(self):
    #     print(self.AccountAPI.get_max_avail_size(instId="BTC-USDT",tdMode="cash"))
    # def test_get_max_size(self):
    #     print(self.AccountAPI.get_maximum_trade_size(instId="BTC-USDT",tdMode="cash"))
    # def test_get_positions(self):
    #     print(self.AccountAPI.get_positions("MARGIN"))
    # def test_set_margin_balance(self):
    #     print(self.AccountAPI.Adjustment_margin(instId="BTC-USDT",posSide="net",type="add",amt="1"))
    # def test_get_lev_info(self):
    #     print(self.AccountAPI.get_leverage("BTC-USDT","cross"));
    # def test_get_max_loan(self):
    #     print(self.AccountAPI.get_max_loan("BTC-USDT","cross","USDT"))
    # def test_get_trade_fee(self):
    #     print(self.AccountAPI.get_fee_rates("SPOT"))
    # def test_get_insterested_accrued(self):
    #     print(self.AccountAPI.get_interest_accrued())
    # def test_get_interestred_rate(self):
    #     print(self.AccountAPI.get_interest_rate())
    # def test_set_greeks(self):
    #     print(self.AccountAPI.set_greeks("BS"))
    #
    # def test_set_isolated_mode(self):
    #     print(self.AccountAPI.set_isolated_mode("automatic","MARGIN"))
    # def test_set_max_withdraw(self):
    #     print(self.AccountAPI.get_max_withdrawal("USDT"))
    # def test_borrow_repay(self):
    #     print(self.AccountAPI.borrow_repay("BTC","borrow","1.0"))
    # def test_borrow_repay_history(self):
    #     print(self.AccountAPI.get_borrow_repay_history())
    # def test_get_interest_limits(self):
    #     print(self.AccountAPI.get_interest_limits())
    # def test_simulated_margin(self):
    #     print(self.AccountAPI.get_simulated_margin())
    # def test_get_greeks(self):
    #     print(self.AccountAPI.get_greeks())
    # '''
    # def test_simulated_margin(self):
    #     print(self.AccountAPI.get_simulated_margin())

    # def test_get_VIP_interest_accrued_data(self):
    #     print(self.AccountAPI.get_VIP_interest_accrued_data())

    # def test_get_VIP_interest_deducted_data(self):
    #     print(self.AccountAPI.get_VIP_interest_deducted_data())

    # def test_get_VIP_loan_order_list(self):
    #     print(self.AccountAPI.get_VIP_loan_order_list())

    # def test_get_VIP_loan_order_detail(self):
    #     print(self.AccountAPI.get_VIP_loan_order_detail(ordId='1'))

    # def test_set_risk_offset_typel(self):
    #     print(self.AccountAPI.set_risk_offset_typel(type='1'))
    #
    # def test_set_auto_loan(self):
    #     print(self.AccountAPI.set_auto_loan())
    #
    # def test_activate_option(self):
    #     print(self.AccountAPI.activate_option())

    # def test_get_max_avaliable_size(self):
    #     print(self.AccountAPI.get_max_avail_size(instId="BTC-USDT",tdMode="cash",quickMgnType='manual'))
    # def test_borrow_repay(self):
    #     print(self.AccountAPI.borrow_repay("BTC", "borrow", "1.0"))

    # def test_simulated_margin(self):
    #     print(self.AccountAPI.get_simulated_margin(spotOffsetType='3'))
    # def test_get_fix_loan_borrowing_limit(self):
    #     logger.debug(f'{self.AccountAPI.get_fix_loan_borrowing_limit()}')
    # def test_get_fix_loan_borrowing_quote(self):
    #     logger.debug(f'{self.AccountAPI.get_fix_loan_borrowing_quote(type="normal")}')
    # def test_place_fix_loan_borrowing_order(self):
    #     logger.debug(f'{self.AccountAPI.place_fix_loan_borrowing_order(ccy="BTC", amt="0.1515", maxRate="0.001", term="30D", reborrow=True, reborrowRate="0.01")}')
    # def test_amend_fix_loan_borrowing_order(self):
    #     logger.debug(f'{self.AccountAPI.amend_fix_loan_borrowing_order(ordId="2407301043344857",reborrow=True,renewMaxRate="0.01")}')
    # def test_fix_loan_manual_reborrow(self):
    #     logger.debug(f'{self.AccountAPI.fix_loan_manual_reborrow(ordId="2407301043344857",maxRate="0.1")}')
    # def test_repay_fix_loan_borrowing_order(self):
    #     logger.info(f'{self.AccountAPI.repay_fix_loan_borrowing_order(ordId="2407301054407907")}')
    # def test_get_fix_loan_borrowing_orders_list(self):
    #     logger.debug(self.AccountAPI.get_fix_loan_borrowing_orders_list(ordId="2407301054407907"))

    # def test_spot_manual_borrow_repay(self):
    #     logger.debug(f'{self.AccountAPI.spot_manual_borrow_repay(ccy="USDT",side="borrow",amt=1)}')
    # def test_set_auto_repay(self):
    #     logger.info(f'{self.AccountAPI.set_auto_repay(autoRepay=True)}')
    # def test_spot_borrow_repay_history(self):
    #     logger.debug(self.AccountAPI.spot_borrow_repay_history(ccy="USDT",type="auto_borrow",after="1597026383085"))

if __name__ == '__main__':
    unittest.main()
