import asyncio

from okx.websocket.WsPrivateAsync import WsPrivateAsync


def privateCallback(message):
    print("privateCallback", message)


async def main():
    """订阅测试"""
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
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    await ws.subscribe(args, callback=privateCallback)
    await asyncio.sleep(30)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg2]
    await ws.unsubscribe(args2, callback=privateCallback)
    await asyncio.sleep(30)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg3]
    await ws.unsubscribe(args3, callback=privateCallback)
    await asyncio.sleep(1)
    await ws.stop()


async def test_place_order():
    """
    测试下单功能
    URL: /ws/v5/private (限速: 60次/秒)
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
    
    # 下单参数
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
    测试批量下单功能
    URL: /ws/v5/private (限速: 60次/秒, 最多20个订单)
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
    
    # 批量下单参数 (最多20个)
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
    测试撤单功能
    URL: /ws/v5/private (限速: 60次/秒)
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
    
    # 撤单参数 (ordId 和 clOrdId 必须传一个)
    cancel_args = [{
        "instId": "BTC-USDT",
        "ordId": "your_order_id"
        # 或者使用 "clOrdId": "client_order_001"
    }]
    await ws.cancel_order(cancel_args, callback=privateCallback, id="cancel001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_batch_cancel_orders():
    """
    测试批量撤单功能
    URL: /ws/v5/private (限速: 60次/秒, 最多20个订单)
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
    测试改单功能
    URL: /ws/v5/private (限速: 60次/秒)
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
    
    # 改单参数
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
    测试批量撤销功能
    URL: /ws/v5/business (限速: 1次/秒)
    注意: 此功能使用 business 频道
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
    
    # 批量撤销参数
    mass_cancel_args = [{
        "instType": "SPOT",
        "instFamily": "BTC-USDT"
    }]
    await ws.mass_cancel(mass_cancel_args, callback=privateCallback, id="massCancel001")
    await asyncio.sleep(5)
    await ws.stop()


async def test_send_method():
    """测试通用send方法"""
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
    
    # 使用通用send方法下单 - 注意要传入callback才能收到响应
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
    asyncio.run(test_mass_cancel())  # 注意使用 business 频道
    asyncio.run(test_send_method())
