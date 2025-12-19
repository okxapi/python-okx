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
    # Withdrawal info channel subscription example, supporting the toAddrType parameter
    # toAddrType: Address type
    # 1: Wallet address, email, phone number or login account name
    # 2: UID (applicable only when dest=3)
    arg4 = {"channel": "withdrawal-info", "ccy": "USDT", "toAddrType": "1"}
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    args.append(arg4)
    await ws.subscribe(args, callback=privateCallback)
    await asyncio.sleep(30)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg2]
    await ws.unsubscribe(args2, callback=privateCallback)
    await asyncio.sleep(30)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg3]
    await ws.unsubscribe(args3, callback=privateCallback)


if __name__ == '__main__':
    asyncio.run(main())
