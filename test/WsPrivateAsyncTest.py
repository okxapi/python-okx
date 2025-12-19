import asyncio

from okx.websocket.WsPrivateAsync import WsPrivateAsync


def privateCallback(message):
    print("privateCallback", message)


async def main():
    """Subscription test"""
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
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
    # Use id parameter to identify unsubscribe request
    await ws.unsubscribe(args2, callback=privateCallback, id="privateUnsub001")
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg3]
    await ws.unsubscribe(args3, callback=privateCallback)
    await asyncio.sleep(1)
    await ws.stop()


async def test_place_order():
    """
    Test place order functionality
    URL: /ws/v5/private (Rate limit: 60 requests/second)
    """
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
    )
    await ws.start()
    await ws.login()
    await asyncio.sleep(5)

    # Order parameters
    order_args = [{
        "instId": "BTC-USDT",
        "tdMode": "cash",
        "clOrdId": "client_order_001",
        "side": "buy",
        "ordType": "limit",
        "sz": "0.001",
        "px": "30000"
    }]
    await ws.place_order(order_args, callback=privateCallback, id="order001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_batch_orders():
    """
    Test batch orders functionality
    URL: /ws/v5/private (Rate limit: 60 requests/second, max 20 orders)
    """
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
    )
    await ws.start()
    await ws.login()
    await asyncio.sleep(5)

    # Batch order parameters (max 20)
    order_args = [
        {
            "instId": "BTC-USDT",
            "tdMode": "cash",
            "clOrdId": "batch_order_001",
            "side": "buy",
            "ordType": "limit",
            "sz": "0.001",
            "px": "30000"
        },
        {
            "instId": "ETH-USDT",
            "tdMode": "cash",
            "clOrdId": "batch_order_002",
            "side": "buy",
            "ordType": "limit",
            "sz": "0.01",
            "px": "2000"
        }
    ]
    await ws.batch_orders(order_args, callback=privateCallback, id="batchOrder001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_cancel_order():
    """
    Test cancel order functionality
    URL: /ws/v5/private (Rate limit: 60 requests/second)
    """
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
    )
    await ws.start()
    await ws.login()
    await asyncio.sleep(5)

    # Cancel order parameters (either ordId or clOrdId must be provided)
    cancel_args = [{
        "instId": "BTC-USDT",
        "ordId": "your_order_id"
        # Or use "clOrdId": "client_order_001"
    }]
    await ws.cancel_order(cancel_args, callback=privateCallback, id="cancel001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_batch_cancel_orders():
    """
    Test batch cancel orders functionality
    URL: /ws/v5/private (Rate limit: 60 requests/second, max 20 orders)
    """
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
    )
    await ws.start()
    await ws.login()
    await asyncio.sleep(5)

    cancel_args = [
        {"instId": "BTC-USDT", "ordId": "order_id_1"},
        {"instId": "ETH-USDT", "ordId": "order_id_2"}
    ]
    await ws.batch_cancel_orders(cancel_args, callback=privateCallback, id="batchCancel001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_amend_order():
    """
    Test amend order functionality
    URL: /ws/v5/private (Rate limit: 60 requests/second)
    """
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
    )
    await ws.start()
    await ws.login()
    await asyncio.sleep(5)

    # Amend order parameters
    amend_args = [{
        "instId": "BTC-USDT",
        "ordId": "your_order_id",
        "newSz": "0.002",
        "newPx": "31000"
    }]
    await ws.amend_order(amend_args, callback=privateCallback, id="amend001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_mass_cancel():
    """
    Test mass cancel functionality
    URL: /ws/v5/business (Rate limit: 1 request/second)
    Note: This function uses the business channel
    """
    url = "wss://wspap.okx.com:8443/ws/v5/business?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
    )
    await ws.start()
    await ws.login()
    await asyncio.sleep(5)

    # Mass cancel parameters
    mass_cancel_args = [{
        "instType": "SPOT",
        "instFamily": "BTC-USDT"
    }]
    await ws.mass_cancel(mass_cancel_args, callback=privateCallback, id="massCancel001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_send_method():
    """Test generic send method"""
    url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    ws = WsPrivateAsync(
        apiKey="your apiKey",
        passphrase="your passphrase",
        secretKey="your secretKey",
        url=url,
        debug=True
    )
    await ws.start()
    await ws.login()
    await asyncio.sleep(5)

    # Use generic send method to place order - callback must be provided to receive response
    order_args = [{
        "instId": "BTC-USDT",
        "tdMode": "cash",
        "side": "buy",
        "ordType": "limit",
        "sz": "0.001",
        "px": "30000"
    }]
    await ws.send("order", order_args, callback=privateCallback, id="send001")
    await asyncio.sleep(5)
    await ws.stop()


if __name__ == '__main__':
    # asyncio.run(main())
    asyncio.run(test_place_order())
    asyncio.run(test_batch_orders())
    asyncio.run(test_cancel_order())
    asyncio.run(test_batch_cancel_orders())
    asyncio.run(test_amend_order())
    asyncio.run(test_mass_cancel())  # Note: uses business channel
    asyncio.run(test_send_method())
