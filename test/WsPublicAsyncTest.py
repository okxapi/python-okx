import asyncio

from okx.websocket.WsPublicAsync import WsPublicAsync


def publicCallback(message):
    print("publicCallback", message)


async def main():
    
    # url = "wss://wspap.okex.com:8443/ws/v5/public?brokerId=9999"
    url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"
    ws = WsPublicAsync(url=url)
    await ws.start()
    args = []
    arg1 = {"channel": "instruments", "instType": "FUTURES"}
    arg2 = {"channel": "instruments", "instType": "SPOT"}
    arg3 = {"channel": "tickers", "instId": "BTC-USDT-SWAP"}
    arg4 = {"channel": "tickers", "instId": "ETH-USDT"}
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    args.append(arg4)
    # 使用 id 参数来标识订阅请求，响应中会返回相同的 id
    await ws.subscribe(args, publicCallback, id="sub001")
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg4]
    # 使用 id 参数来标识取消订阅请求
    await ws.unsubscribe(args2, publicCallback, id="unsub001")
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg2, arg3]
    await ws.unsubscribe(args3, publicCallback)
    await asyncio.sleep(1)
    # 正确关闭 websocket 连接
    await ws.stop()


if __name__ == '__main__':
    asyncio.run(main())
