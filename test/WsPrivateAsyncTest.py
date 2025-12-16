import asyncio

from okx.websocket.WsPrivateAsync import WsPrivateAsync


def privateCallback(message):
    print("privateCallback", message)


async def main():
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        useServerTime=False
    )
    await ws.start()
    args = []
    arg1 = {"channel": "account", "ccy": "BTC"}
    arg2 = {"channel": "orders", "instType": "ANY"}
    arg3 = {"channel": "balance_and_position"}
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    # 使用 id 参数来标识订阅请求，响应中会返回相同的 id
    # 注意：id 只能包含字母和数字，不能包含下划线等特殊字符
    await ws.subscribe(args, callback=privateCallback, id="privateSub001")
    await asyncio.sleep(10)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg2]
    # 使用 id 参数来标识取消订阅请求
    await ws.unsubscribe(args2, callback=privateCallback, id="privateUnsub001")
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg3]
    await ws.unsubscribe(args3, callback=privateCallback, id="privateUnsub002")
    await asyncio.sleep(1)
    # 正确关闭 websocket 连接
    await ws.stop()


if __name__ == '__main__':
    asyncio.run(main())
