"""
Unit tests for okx.Trade v5 API sync batch (0.4.3) — items #1, #3, #5, #7.

Mirrors the existing @patch.object mock pattern in test/unit/okx/test_trade.py.
All new params are additive/opt-in: unset => omitted from the request (byte-identical
to 0.4.2 for existing callers).
"""
import unittest
from unittest.mock import patch
from okx.Trade import TradeAPI
from okx import consts as c

# Placeholder client identifiers — every request is mocked (see @patch.object),
# so these dummy strings are never signed or transmitted; not real credentials.
_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'

_REQUIRED_PLACE_ORDER = dict(instId='BTC-USDT', tdMode='cash', side='buy', ordType='limit', sz='1')


class _Base(unittest.TestCase):
    def setUp(self):
        self.api = TradeAPI(api_key=_STUB_ID, api_secret_key=_STUB_SIGN, passphrase=_STUB_PHRASE, flag='0')


class TestPlaceOrderNewParams(_Base):
    """#3 isElpTakerAccess, #5 instIdCode on place_order"""

    @patch.object(TradeAPI, '_request_with_params')
    def test_place_order_backward_compatible_omits_new_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.place_order(**_REQUIRED_PLACE_ORDER)
        params = mock_request.call_args[0][2]
        self.assertNotIn('isElpTakerAccess', params)
        self.assertNotIn('instIdCode', params)
        self.assertNotIn('tradeQuoteCcy', params)
        self.assertIn('attachAlgoOrds', params)

    @patch.object(TradeAPI, '_request_with_params')
    def test_place_order_isElpTakerAccess_written_when_set(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.place_order(**_REQUIRED_PLACE_ORDER, isElpTakerAccess=True)
        params = mock_request.call_args[0][2]
        self.assertEqual(params['isElpTakerAccess'], True)

    @patch.object(TradeAPI, '_request_with_params')
    def test_place_order_instIdCode_written_when_set(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.place_order(**_REQUIRED_PLACE_ORDER, instIdCode='123')
        params = mock_request.call_args[0][2]
        self.assertEqual(params['instIdCode'], '123')
        self.assertEqual(mock_request.call_args[0][1], c.PLACR_ORDER)


class TestPlaceAlgoOrderNewParams(_Base):
    """#1 advanceOrdType, #5 tpTriggerRatio/slTriggerRatio on place_algo_order"""

    @patch.object(TradeAPI, '_request_with_params')
    def test_algo_backward_compatible_omits_new_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.place_algo_order(instId='BTC-USDT', tdMode='cash', side='buy', ordType='conditional', sz='1')
        params = mock_request.call_args[0][2]
        self.assertNotIn('advanceOrdType', params)
        self.assertNotIn('tpTriggerRatio', params)
        self.assertNotIn('slTriggerRatio', params)

    @patch.object(TradeAPI, '_request_with_params')
    def test_algo_advanceOrdType_written_when_set(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.place_algo_order(instId='BTC-USDT', tdMode='cash', side='buy',
                                  ordType='trigger', sz='1', advanceOrdType='fok')
        params = mock_request.call_args[0][2]
        self.assertEqual(params['advanceOrdType'], 'fok')
        self.assertEqual(mock_request.call_args[0][1], c.PLACE_ALGO_ORDER)

    @patch.object(TradeAPI, '_request_with_params')
    def test_algo_trigger_ratios_written_when_set(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.place_algo_order(instId='BTC-USDT', tdMode='cash', side='buy', ordType='oco',
                                  sz='1', tpTriggerRatio='0.1', slTriggerRatio='0.05')
        params = mock_request.call_args[0][2]
        self.assertEqual(params['tpTriggerRatio'], '0.1')
        self.assertEqual(params['slTriggerRatio'], '0.05')


class TestAmendOrderNewParams(_Base):
    """#5 newTpTriggerRatio/newSlTriggerRatio on amend_order"""

    @patch.object(TradeAPI, '_request_with_params')
    def test_amend_backward_compatible_omits_new_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.amend_order(instId='BTC-USDT', ordId='1')
        params = mock_request.call_args[0][2]
        self.assertNotIn('newTpTriggerRatio', params)
        self.assertNotIn('newSlTriggerRatio', params)

    @patch.object(TradeAPI, '_request_with_params')
    def test_amend_trigger_ratios_written_when_set(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.amend_order(instId='BTC-USDT', ordId='1',
                             newTpTriggerRatio='0.2', newSlTriggerRatio='0.1')
        params = mock_request.call_args[0][2]
        self.assertEqual(params['newTpTriggerRatio'], '0.2')
        self.assertEqual(params['newSlTriggerRatio'], '0.1')
        self.assertEqual(mock_request.call_args[0][1], c.AMEND_ORDER)


class TestOneClickRepayNew(_Base):
    """#7 one-click-repay-new endpoints"""

    @patch.object(TradeAPI, '_request_without_params')
    def test_get_oneclick_repay_list_new(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_oneclick_repay_list_new()
        mock_request.assert_called_once_with(c.GET, c.ONE_CLICK_REPAY_SUPPORT_NEW)

    @patch.object(TradeAPI, '_request_with_params')
    def test_oneclick_repay_new(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.oneclick_repay_new(debtCcy='USDT', repayCcyList=['BTC'])
        mock_request.assert_called_once_with(
            c.POST, c.ONE_CLICK_REPAY_NEW,
            {'debtCcy': 'USDT', 'repayCcyList': ['BTC']})


if __name__ == '__main__':
    unittest.main()
