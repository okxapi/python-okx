import hmac
import base64
import datetime
from . import consts as c


def sign(message, secretKey):
    mac = hmac.new(bytes(secretKey, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


def pre_hash(timestamp, method, request_path, body,debug = True):
    if debug == True:
        print('body: ',body)
    return str(timestamp) + str.upper(method) + request_path + body


def get_header(api_key, sign, timestamp, passphrase, flag,debug = True):
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_JSON
    header[c.OK_ACCESS_KEY] = api_key
    header[c.OK_ACCESS_SIGN] = sign
    header[c.OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[c.OK_ACCESS_PASSPHRASE] = passphrase
    header['x-simulated-trading'] = flag
    if debug == True:
        print('header: ',header)
    return header

def get_header_no_sign(flag,debug = True):
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_JSON
    header['x-simulated-trading'] = flag
    if debug == True:
        print('header: ',header)
    return header

def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        if(value != ''):
            url = url + str(key) + '=' + str(value) + '&'
    url = url[0:-1]
    #print('url:',url)
    return url


def get_timestamp():
    now = datetime.datetime.utcnow()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)

    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()

    return base64.b64encode(d)
