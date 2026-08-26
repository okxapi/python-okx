from .okxclient import OkxClient
from .consts import *


class AffiliateAPI(OkxClient):
    def __init__(self, api_key='-1', api_secret_key='-1', passphrase='-1', use_server_time=None, flag='1',
                 domain='https://www.okx.com', debug=False, proxy=None):
        OkxClient.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag, domain, debug, proxy)

    def get_invitee_detail(self, uid):
        params = {'uid': uid}
        return self._request_with_params(GET, AFFILIATE_TVB_INVITEE_DETAIL, params)

    def get_invitee_list(self, periodType='', begin='', end='', feeTier=None, tradeType='',
                         keyword='', orderBy='', orderDir='', page='', limit=''):
        params = {}
        if periodType != '':
            params['periodType'] = periodType
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        if feeTier is not None:
            params['feeTier'] = feeTier
        if tradeType != '':
            params['tradeType'] = tradeType
        if keyword != '':
            params['keyword'] = keyword
        if orderBy != '':
            params['orderBy'] = orderBy
        if orderDir != '':
            params['orderDir'] = orderDir
        if page != '':
            params['page'] = page
        if limit != '':
            params['limit'] = limit
        return self._request_with_params(GET, AFFILIATE_TVB_INVITEE_LIST, params)

    def get_link_list(self, periodType='', begin='', end='', page='', limit='',
                      linkType='', linkStatus=''):
        params = {}
        if periodType != '':
            params['periodType'] = periodType
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        if page != '':
            params['page'] = page
        if limit != '':
            params['limit'] = limit
        if linkType != '':
            params['linkType'] = linkType
        if linkStatus != '':
            params['linkStatus'] = linkStatus
        return self._request_with_params(GET, AFFILIATE_TVB_LINK_LIST, params)

    def get_performance_summary(self, periodType='', begin='', end=''):
        params = {}
        if periodType != '':
            params['periodType'] = periodType
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        return self._request_with_params(GET, AFFILIATE_TVB_PERFORMANCE_SUMMARY, params)

    def get_tier_breakdown(self, periodType='', begin='', end=''):
        params = {}
        if periodType != '':
            params['periodType'] = periodType
        if begin != '':
            params['begin'] = begin
        if end != '':
            params['end'] = end
        return self._request_with_params(GET, AFFILIATE_TVB_TIER_BREAKDOWN, params)
