import asyncio

from okx.websocket.WsPublicAsync import WsPublicAsync


def publicCallback(message):
    print("publicCallback", message)


async def main():
    # url = "wss://wspap.okex.com:8443/ws/v5/public?brokerId=9999"
    url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"
    ws = WsPublicAsync(url=url, debug=True)  # 开启debug日志
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
    await ws.subscribe(args, publicCallback)
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg4]
    await ws.unsubscribe(args2, publicCallback)
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg2, arg3]
    await ws.unsubscribe(args3, publicCallback)
    await asyncio.sleep(1)
    await ws.stop()


async def test_business_channel_with_login():
    """
    测试 business 频道的登录功能
    business 频道需要登录后才能订阅某些私有数据
    """
    url = "wss://wspap.okx.com:8443/ws/v5/business?brokerId=9999"
    ws = WsPublicAsync(
        url=url,
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        debug=True
    )
    await ws.start()
    
    # 登录
    await ws.login()
    await asyncio.sleep(5)
    
    # 订阅需要登录的频道
    args = [{"channel": "candle1m", "instId": "BTC-USDT"}]
    await ws.subscribe(args, publicCallback)
    await asyncio.sleep(30)
    await ws.stop()


async def test_send_method():
    """测试通用send方法"""
    url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"
    ws = WsPublicAsync(url=url, debug=True)
    await ws.start()
    
    # 使用通用send方法订阅 - 注意要传入callback才能收到响应
    args = [{"channel": "tickers", "instId": "BTC-USDT"}]
    await ws.send("subscribe", args, callback=publicCallback, id="send001")
    await asyncio.sleep(10)
    await ws.stop()


if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(test_business_channel_with_login())
    asyncio.run(test_send_method())
