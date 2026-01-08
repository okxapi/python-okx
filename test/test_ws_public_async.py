import asyncio

from okx.websocket.WsPublicAsync import WsPublicAsync


def publicCallback(message):
    print("publicCallback", message)


async def main():
    # url = "wss://wspap.okex.com:8443/ws/v5/public?brokerId=9999"
    url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"
    ws = WsPublicAsync(url=url, debug=True)  # Enable debug logging
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
    # Use id parameter to identify subscribe request, the same id will be returned in response
    await ws.subscribe(args, publicCallback, id="sub001")
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg4]
    # Use id parameter to identify unsubscribe request
    await ws.unsubscribe(args2, publicCallback, id="unsub001")
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg2, arg3]
    await ws.unsubscribe(args3, publicCallback)
    await asyncio.sleep(1)
    await ws.stop()


async def test_business_channel_with_login():
    """
    Test business channel login functionality
    Business channel requires login to subscribe to certain private data
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

    # Login
    await ws.login()
    await asyncio.sleep(5)

    # Subscribe to channels that require login
    args = [{"channel": "candle1m", "instId": "BTC-USDT"}]
    await ws.subscribe(args, publicCallback)
    await asyncio.sleep(30)
    await ws.stop()


async def test_send_method():
    """Test generic send method"""
    url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"
    ws = WsPublicAsync(url=url, debug=True)
    await ws.start()

    # Use generic send method to subscribe - callback must be provided to receive response
    args = [{"channel": "tickers", "instId": "BTC-USDT"}]
    await ws.send("subscribe", args, callback=publicCallback, id="send001")
    await asyncio.sleep(10)
    await ws.stop()


if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(test_business_channel_with_login())
    asyncio.run(test_send_method())
