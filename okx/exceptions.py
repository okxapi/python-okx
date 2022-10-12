# coding=utf-8


class OkxAPIException(Exception):

    def __init__(self, response):
        print(response.text + ', ' + str(response.status_code))
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Okx: {}'.format(response.text)
        else:
            if "code" in json_res.keys() and "msg" in json_res.keys():
                self.code = json_res['code']
                self.message = json_res['msg']
            else:
                self.code = 'None'
                self.message = 'System error'

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'API Request Error(code=%s): %s' % (self.code, self.message)


class OkxRequestException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'OkxRequestException: %s' % self.message


class OkxParamsException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'OkxParamsException: %s' % self.message
