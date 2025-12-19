import asyncio
import json
import logging
import warnings

from okx.websocket import WsUtils
from okx.websocket.WebSocketFactory import WebSocketFactory

logger = logging.getLogger(__name__)


class WsPrivateAsync:
    def __init__(self, apiKey, passphrase, secretKey, url, useServerTime=None, debug=False):
        self.url = url
        self.subscriptions = set()
        self.callback = None
        self.loop = asyncio.get_event_loop()
        self.factory = WebSocketFactory(url)
        self.apiKey = apiKey
        self.passphrase = passphrase
        self.secretKey = secretKey
        self.useServerTime = False
        self.websocket = None
        self.debug = debug

        # 设置日志级别
        if debug:
            logger.setLevel(logging.DEBUG)

        # 废弃 useServerTime 参数警告
        if useServerTime is not None:
            warnings.warn("useServerTime parameter is deprecated. Please remove it.", DeprecationWarning)

    async def connect(self):
        self.websocket = await self.factory.connect()

    async def consume(self):
        async for message in self.websocket:
            if self.debug:
                logger.debug("Received message: {%s}", message)
            if self.callback:
                self.callback(message)

    async def subscribe(self, params: list, callback, id: str = None):
        self.callback = callback

        logRes = await self.login()
        await asyncio.sleep(5)
        if logRes:
            payload_dict = {
                "op": "subscribe",
                "args": params
            }
            if id is not None:
                payload_dict["id"] = id
            payload = json.dumps(payload_dict)
            if self.debug:
                logger.debug(f"subscribe: {payload}")
            await self.websocket.send(payload)
        # await self.consume()

    async def login(self):
        loginPayload = WsUtils.initLoginParams(
            useServerTime=self.useServerTime,
            apiKey=self.apiKey,
            passphrase=self.passphrase,
            secretKey=self.secretKey
        )
        if self.debug:
            logger.debug(f"login: {loginPayload}")
        await self.websocket.send(loginPayload)
        return True

    async def unsubscribe(self, params: list, callback, id: str = None):
        self.callback = callback
        payload_dict = {
            "op": "unsubscribe",
            "args": params
        }
        if id is not None:
            payload_dict["id"] = id
        payload = json.dumps(payload_dict)
        if self.debug:
            logger.debug(f"unsubscribe: {payload}")
        else:
            logger.info(f"unsubscribe: {payload}")
        await self.websocket.send(payload)

    async def send(self, op: str, args: list, callback=None, id: str = None):
        """
        通用发送方法
        :param op: 操作类型
        :param args: 参数列表
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        payload_dict = {
            "op": op,
            "args": args
        }
        if id is not None:
            payload_dict["id"] = id
        payload = json.dumps(payload_dict)
        if self.debug:
            logger.debug(f"send: {payload}")
        await self.websocket.send(payload)

    async def place_order(self, args: list, callback=None, id: str = None):
        """
        下单
        :param args: 下单参数列表
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        await self.send("order", args, id=id)

    async def batch_orders(self, args: list, callback=None, id: str = None):
        """
        批量下单
        :param args: 批量下单参数列表
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        await self.send("batch-orders", args, id=id)

    async def cancel_order(self, args: list, callback=None, id: str = None):
        """
        撤单
        :param args: 撤单参数列表
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        await self.send("cancel-order", args, id=id)

    async def batch_cancel_orders(self, args: list, callback=None, id: str = None):
        """
        批量撤单
        :param args: 批量撤单参数列表
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        await self.send("batch-cancel-orders", args, id=id)

    async def amend_order(self, args: list, callback=None, id: str = None):
        """
        改单
        :param args: 改单参数列表
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        await self.send("amend-order", args, id=id)

    async def batch_amend_orders(self, args: list, callback=None, id: str = None):
        """
        批量改单
        :param args: 批量改单参数列表
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        await self.send("batch-amend-orders", args, id=id)

    async def mass_cancel(self, args: list, callback=None, id: str = None):
        """
        Mass cancel (批量撤销)
        注意：此方法用于 /ws/v5/business 频道，限速 1次/秒
        :param args: 撤销参数列表，包含 instType 和 instFamily
        :param callback: 回调函数
        :param id: 可选的请求ID
        """
        if callback:
            self.callback = callback
        await self.send("mass-cancel", args, id=id)

    async def stop(self):
        await self.factory.close()

    async def start(self):
        if self.debug:
            logger.debug("Connecting to WebSocket...")
        else:
            logger.info("Connecting to WebSocket...")
        await self.connect()
        self.loop.create_task(self.consume())

    def stop_sync(self):
        if self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.stop(), self.loop)
            future.result(timeout=10)
        else:
            self.loop.run_until_complete(self.stop())
