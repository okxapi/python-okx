"""
Unit tests for okx.Affiliate AffiliateAPI — TD 0.4.4 items #12-16
(GET affiliate/tvb/invitee/detail, invitee/list, link/list, performance/summary,
tier-breakdown).
"""
import unittest
from unittest.mock import patch
from okx.Affiliate import AffiliateAPI
from okx import consts as c

_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestAffiliateAPI(unittest.TestCase):
    def setUp(self):
        self.api = AffiliateAPI(
            api_key=_STUB_ID,
            api_secret_key=_STUB_SIGN,
            passphrase=_STUB_PHRASE,
            flag='0',
        )

    def test_constant_paths(self):
        self.assertEqual(c.AFFILIATE_TVB_INVITEE_DETAIL, '/api/v5/affiliate/tvb/invitee/detail')
        self.assertEqual(c.AFFILIATE_TVB_INVITEE_LIST, '/api/v5/affiliate/tvb/invitee/list')
        self.assertEqual(c.AFFILIATE_TVB_LINK_LIST, '/api/v5/affiliate/tvb/link/list')
        self.assertEqual(c.AFFILIATE_TVB_PERFORMANCE_SUMMARY, '/api/v5/affiliate/tvb/performance/summary')
        self.assertEqual(c.AFFILIATE_TVB_TIER_BREAKDOWN, '/api/v5/affiliate/tvb/tier-breakdown')

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_invitee_detail(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_invitee_detail(uid='123456')
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_INVITEE_DETAIL, {'uid': '123456'})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_invitee_list_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_invitee_list()
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_INVITEE_LIST, {})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_invitee_list_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        fee_tier = ['0', '10']
        self.api.get_tvb_invitee_list(
            periodType='custom', begin='1', end='2', feeTier=fee_tier,
            tradeType='SPOT', keyword='abc', orderBy='validVol',
            orderDir='asc', page='2', limit='50')
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_INVITEE_LIST,
            {'periodType': 'custom', 'begin': '1', 'end': '2', 'feeTier': fee_tier,
             'tradeType': 'SPOT', 'keyword': 'abc', 'orderBy': 'validVol',
             'orderDir': 'asc', 'page': '2', 'limit': '50'})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_link_list_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_link_list()
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_LINK_LIST, {})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_link_list_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_link_list(
            periodType='last_7d', begin='1', end='2', page='1', limit='100',
            linkType='standard', linkStatus='normal')
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_LINK_LIST,
            {'periodType': 'last_7d', 'begin': '1', 'end': '2', 'page': '1',
             'limit': '100', 'linkType': 'standard', 'linkStatus': 'normal'})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_performance_summary_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_performance_summary()
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_PERFORMANCE_SUMMARY, {})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_performance_summary_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_performance_summary(periodType='custom', begin='1', end='2')
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_PERFORMANCE_SUMMARY,
            {'periodType': 'custom', 'begin': '1', 'end': '2'})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_tier_breakdown_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_tier_breakdown()
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_TIER_BREAKDOWN, {})

    @patch.object(AffiliateAPI, '_request_with_params')
    def test_get_tvb_tier_breakdown_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_tvb_tier_breakdown(periodType='this_month', begin='1', end='2')
        mock_request.assert_called_once_with(
            c.GET, c.AFFILIATE_TVB_TIER_BREAKDOWN,
            {'periodType': 'this_month', 'begin': '1', 'end': '2'})


if __name__ == '__main__':
    unittest.main()
