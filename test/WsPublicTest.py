import time

from okx.websocket.WsPublic import WsPublic


def publicCallback(message):
    print("publicCallback", message)


if __name__ == '__main__':
    #url = "wss://wspri.coinall.ltd:8443/ws/v5/ipublic?brokerId=9999"
    url = "wss://wspap.okx.com:8443/ws/v5/public"
    ws = WsPublic(url=url)
    ws.start()
    args = []
    arg1 = {"channel": "instruments", "instType": "FUTURES"}
    arg2 = {"channel": "instruments", "instType": "SPOT"}
    arg3 = {"channel": "tickers", "instId": "BTC-USDT"}
    arg4 = {"channel": "tickers", "instId": "ETH-USDT"}
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    args.append(arg4)
    ws.subscribe(args, publicCallback)
    time.sleep(10)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg4]
    ws.unsubscribe(args2, publicCallback)
    time.sleep(10)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg2, arg3]
    ws.unsubscribe(args3, publicCallback)
