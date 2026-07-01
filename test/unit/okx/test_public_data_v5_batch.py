"""
Unit tests for okx.PublicData get_announcements — item #11.
"""
import unittest
from unittest.mock import patch
from okx.PublicData import PublicAPI
from okx import consts as c

# Placeholder client identifiers — every request is mocked; not real credentials.
_STUB_ID = 'test_key'
_STUB_SIGN = 'test_secret'
_STUB_PHRASE = 'test_pass'


class TestGetAnnouncements(unittest.TestCase):
    def setUp(self):
        self.api = PublicAPI(api_key=_STUB_ID, api_secret_key=_STUB_SIGN, passphrase=_STUB_PHRASE, flag='0')

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_announcements_default(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_announcements()
        mock_request.assert_called_once_with(c.GET, c.ANNOUNCEMENTS, {'annType': '', 'page': ''})

    @patch.object(PublicAPI, '_request_with_params')
    def test_get_announcements_with_params(self, mock_request):
        mock_request.return_value = {'code': '0'}
        self.api.get_announcements(annType='announcements-latest-announcements', page='2')
        mock_request.assert_called_once_with(
            c.GET, c.ANNOUNCEMENTS,
            {'annType': 'announcements-latest-announcements', 'page': '2'})


if __name__ == '__main__':
    unittest.main()
