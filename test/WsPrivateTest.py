import time

from okx.websocket.WsPrivate import WsPrivate


def privateCallback(message):
    print("WsPrivate subscribe callback:", message)


if __name__ == '__main__':
    url = "wss://ws.okx.com:8443/ws/v5/private"
    ws = WsPrivate(apiKey="your_apiKey",
                   passphrase="your_passphrase",
                   secretKey="your_secretKey",
                   url=url,
                   useServerTime=False)
    ws.start()
    args = []
    arg1 = {"channel": "account", "instType": "BTC"}
    arg2 = {"channel": "orders", "instType": "ANY"}
    arg3 = {"channel": "balance_and_position"}
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    ws.subscribe(args, callback=privateCallback)
    time.sleep(30)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg2]
    ws.unsubscribe(args2, callback=privateCallback)
    time.sleep(30)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg3]
    ws.unsubscribe(args3, callback=privateCallback)
