"""
Unit tests for okx.Finance.FlexibleLoan FlexibleLoanAPI — TD 0.4.4 items #4-6
(POST flexible-loan/borrow, POST flexible-loan/repay, GET flexible-loan/emode-info).
"""
import unittest
from unittest.mock import patch
from okx.Finance.FlexibleLoan import FlexibleLoanAPI
from okx import consts as c

_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestFlexibleLoanBorrow(unittest.TestCase):
    def setUp(self):
        self.api = FlexibleLoanAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0',
        )

    def test_borrow_constant_path(self):
        self.assertEqual(c.FINANCE_FLEXIBLE_LOAN_BORROW,
                         '/api/v5/finance/flexible-loan/borrow')

    @patch.object(FlexibleLoanAPI, '_request_with_params')
    def test_borrow_create_order(self, mock_request):
        mock_request.return_value = {'code': '0'}
        loan_data = {'ccy': 'USDT', 'amt': '100'}
        collateral = [{'ccy': 'BTC', 'amt': '0.01'}]
        self.api.borrow(loanData=loan_data, clOrdId='abc123',
                        collateralData=collateral, eMode='0')
        mock_request.assert_called_once_with(
            c.POST, c.FINANCE_FLEXIBLE_LOAN_BORROW,
            {'loanData': loan_data, 'clOrdId': 'abc123',
             'collateralData': collateral, 'eMode': '0'})

    @patch.object(FlexibleLoanAPI, '_request_with_params')
    def test_borrow_required_only(self, mock_request):
        mock_request.return_value = {'code': '0'}
        loan_data = {'ccy': 'USDT', 'amt': '50'}
        self.api.borrow(loanData=loan_data, clOrdId='xyz')
        mock_request.assert_called_once_with(
            c.POST, c.FINANCE_FLEXIBLE_LOAN_BORROW,
            {'loanData': loan_data, 'clOrdId': 'xyz'})

    @patch.object(FlexibleLoanAPI, '_request_with_params')
    def test_borrow_add_to_existing_order(self, mock_request):
        mock_request.return_value = {'code': '0'}
        loan_data = {'ccy': 'USDT', 'amt': '25'}
        self.api.borrow(loanData=loan_data, clOrdId='k2', ordId='ord-1')
        mock_request.assert_called_once_with(
            c.POST, c.FINANCE_FLEXIBLE_LOAN_BORROW,
            {'loanData': loan_data, 'clOrdId': 'k2', 'ordId': 'ord-1'})


class TestFlexibleLoanRepay(unittest.TestCase):
    def setUp(self):
        self.api = FlexibleLoanAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0',
        )

    def test_repay_constant_path(self):
        self.assertEqual(c.FINANCE_FLEXIBLE_LOAN_REPAY,
                         '/api/v5/finance/flexible-loan/repay')

    @patch.object(FlexibleLoanAPI, '_request_with_params')
    def test_repay_builds_request(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.repay(ordId='ord-1', ccy='USDT', amt='10', clOrdId='r1')
        mock_request.assert_called_once_with(
            c.POST, c.FINANCE_FLEXIBLE_LOAN_REPAY,
            {'ordId': 'ord-1', 'ccy': 'USDT', 'amt': '10', 'clOrdId': 'r1'})


class TestFlexibleLoanEmodeInfo(unittest.TestCase):
    def setUp(self):
        self.api = FlexibleLoanAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0',
        )

    def test_emode_info_constant_path(self):
        self.assertEqual(c.FINANCE_FLEXIBLE_LOAN_EMODE_INFO,
                         '/api/v5/finance/flexible-loan/emode-info')

    @patch.object(FlexibleLoanAPI, '_request_without_params')
    def test_emode_info_builds_request(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.emode_info()
        mock_request.assert_called_once_with(
            c.GET, c.FINANCE_FLEXIBLE_LOAN_EMODE_INFO)


if __name__ == '__main__':
    unittest.main()
