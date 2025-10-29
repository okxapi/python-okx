#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETH perpetual trading bot for OKX.

说明（中文）：
- 启动时使用 REST 加载合约元信息、账户余额并转换为 USDT。
- 运行时优先使用 WebSocket 更新持仓、余额、订单与行情：订阅私有频道 positions、balance_and_position、orders，可选 fills；公共频道使用 tickers。
- 下单支持 REST 与 WS 两种发送方式（默认使用 REST），提供批量下单与批量撤单的封装，且在发送前自动限速。
- active_orders 以 orders WS 推送为最终来源；WS 的 op="order"/"batch-orders"/"cancel-order"/"batch-cancel-orders" 的直接响应也会被记录并与 active_orders 关联。
- 提供 Mock 模式（USE_MOCK=1）便于离线测试。

使用：
- 通过环境变量设置 OKX API：OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE
- OKX_FLAG=1 为模拟盘，=0 为实盘
- USE_MOCK=1 使用内置 Mock API，不连接外部服务（推荐初次测试）

作者备注：
- 请先在模拟盘或 USE_MOCK=1 下完成测试，再在实盘运行。
- 切勿在公开场景中泄露 API Secret/Passphrase。
"""

import asyncio
import time
import json
import logging
import string
import random
import os
from datetime import datetime
from collections import defaultdict
from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Optional, Dict, Any, List

# 尝试导入 OKX SDK（私有与公共 WS、Account/Trade/Market）
try:
    from okx.websocket.WsPrivateAsync import WsPrivateAsync as PrivateWs
except Exception:
    PrivateWs = None
try:
    from okx.websocket.WsPublicAsync import WsPublicAsync as PublicWs
except Exception:
    PublicWs = None

try:
    import okx.Account as Account
    import okx.Trade as Trade
    import okx.MarketData as MarketData
except Exception:
    Account = None
    Trade = None
    MarketData = None

getcontext().prec = 28

# -------------------- 配置 & 默认值 --------------------
USE_MOCK = os.getenv("USE_MOCK", "0") == "1"

API_KEY = os.getenv("OKX_API_KEY", "")
SECRET_KEY = os.getenv("OKX_SECRET_KEY", "")
PASSPHRASE = os.getenv("OKX_PASSPHRASE", "")

OKX_FLAG = os.getenv("OKX_FLAG", "1")  # "1" testnet, "0" live

RUN_FOREVER = True

CONTRACT_INFO: Dict[str, Any] = {
    "symbol": "ETH-USDT-SWAP",
    "lotSz": 1,
    "minSz": 0.0,     # will be fetched
    "ctVal": 0.0,     # will be fetched (contract face value)
    "tickSz": 0.0,    # will be fetched
    "ctValCcy": "ETH",
    "instType": "SWAP",
    "instIdCode": None,
    "instFamily": None
}
SYMBOL = CONTRACT_INFO["symbol"]
TICK_SIZE = CONTRACT_INFO["tickSz"]

TRADE_STRATEGY = {
    "price_offset": 0.015,
    "eth_position": 0.01,
    "leverage": 10,
    "order_increment": 0,
    "fixed_trend_direction": "long",
    "trend_mode": "fixed"
}

# -------------------- 日志 --------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "trading.log")

logger = logging.getLogger("eth_trade_bot")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(fh)
    logger.addHandler(ch)


def log_action(action: str, details: str, level: str = "info", extra_data: Optional[dict] = None, exc_info: bool = False):
    symbols = {"debug": "🔵", "info": "🟢", "warning": "🟠", "error": "🔴", "critical": "⛔"}
    symbol = symbols.get(level, "⚪")
    header = "\n" + "-" * 80 + "\n" + f"[{datetime.now().strftime('%H:%M:%S.%f')}] {symbol} {action}"
    line = header + f"\n  • {details}"
    if extra_data is not None:
        try:
            line += f"\n  • 附加数据: {json.dumps(extra_data, ensure_ascii=False, indent=2)}"
        except Exception:
            line += f"\n  • 附加数据: {extra_data}"
    line += "\n" + "-" * 80
    if level == "debug":
        logger.debug(line, exc_info=exc_info)
    elif level == "warning":
        logger.warning(line, exc_info=exc_info)
    elif level == "error":
        logger.error(line, exc_info=exc_info)
    elif level == "critical":
        logger.critical(line, exc_info=exc_info)
    else:
        logger.info(line, exc_info=exc_info)


# -------------------- 全局运行时状态 --------------------
# 账户 USDT 等价总额
account_equity_usdt: float = 0.0
initial_equity_usdt: float = 0.0

# 价格与来源
current_price: float = 0.0
last_price: float = 0.0
price_source: str = "unknown"
last_ws_price_update: float = 0.0
last_api_price_update: float = 0.0

trading_direction = TRADE_STRATEGY.get("fixed_trend_direction", "long")
INSTRUMENTS_LOADED = False

# 订单 / 仓位 存储
active_orders: Dict[str, dict] = {}
order_pair_mapping: Dict[str, dict] = {}
position_info = defaultdict(lambda: {"pos": 0.0, "usdt_value": 0.0, "avg_px": 0.0, "upl": 0.0, "entry_time": 0})

# API clients（initialize_clients 填充）
account_api = None
trade_api = None
market_api = None

# 私有 WS 实例
_ws_instance = None

# 公共 WS 实例（tickers）
_public_ws_instance = None

# seen 去重集合（WS orders / fills）
seen_trade_ids = set()
seen_filled_ordids = set()
seen_reqids = set()

# public tickers 最优价记录
best_bid: float = 0.0
best_ask: float = 0.0

# 是否启用公共行情 WS
ENABLE_PUBLIC_TICKER = True
# 是否订阅 fills 频道（需 VIP5+）
ENABLE_FILLS_CHANNEL = False

# -------------------- 工具函数 --------------------
def safe_float(v, default: float = 0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def generate_order_id(prefix: str) -> str:
    clean = ''.join(c for c in prefix if c.isalnum())
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    ts = int(time.time() * 1000) % 1000000
    return (clean + str(ts) + suffix)[:32]


def round_price(price: float) -> float:
    tick_val = CONTRACT_INFO.get("tickSz", 0) or TICK_SIZE or 0
    try:
        tick = Decimal(str(tick_val))
        p = Decimal(str(price))
        if tick == 0:
            return float(p)
        quant = (p / tick).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        rounded = (quant * tick).normalize()
        return float(rounded)
    except Exception:
        return float(price)


def round_to_min_size(size: float) -> float:
    min_sz = CONTRACT_INFO.get("minSz", 0) or 0
    try:
        m = Decimal(str(min_sz))
        s = Decimal(str(size))
        if m == 0:
            return float(s)
        q = (s / m).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        rounded = (q * m).normalize()
        return float(rounded)
    except Exception:
        return float(size)


def validate_position_size(sz: float) -> float:
    """
    校验下单数量，若小于 minSz 则抛异常或调整为 minSz。
    当前策略：若小于 minSz，则调整到 minSz；你也可以改为抛错终止下单。
    """
    min_sz = CONTRACT_INFO.get("minSz", 0) or 0
    if min_sz <= 0:
        return sz
    if sz <= 0:
        raise ValueError("下单数量必须大于 0")
    # 若小于最小单位，调整为最小单位
    if sz < min_sz:
        sz = min_sz
    return sz


# -------------------- Mock APIs（便于本地测试） --------------------
class MockTradeAPI:
    def place_order(self, **kwargs):
        return {"code": "0", "data": [{"ordId": f"mock_{int(time.time() * 1000)}", "clOrdId": kwargs.get("clOrdId", "")}]} 

    def place_multiple_orders(self, batch):
        return {"code": "0", "data": [{"clOrdId": r.get("clOrdId", ""), "sCode": "0", "ordId": f"mock_{random.randint(1000, 9999)}"} for r in batch]}

    def cancel_order(self, **kwargs):
        return {"code": "0", "data": []}

    def cancel_multiple_orders(self, requests):
        return {"code": "0", "data": []}


class MockAccountAPI:
    def get_account_balance(self, **kwargs):
        # return sample balances: USDT and BTC
        return {"code": "0", "data": [{"details": [{"ccy": "USDT", "eq": "1000.0"}, {"ccy": "BTC", "eq": "0.01"}]}]}

    def get_positions(self, **kwargs):
        return {"code": "0", "data": []}

    def get_instruments(self, **kwargs):
        return {"code": "0", "data": [{"instId": CONTRACT_INFO["symbol"], "minSz": "0.01", "tickSz": "0.01", "ctVal": "0.1", "lotSz": "0.01", "ctValCcy": "ETH", "instIdCode": "2021032601102994", "instFamily": "ETH-USDT"}]} 


class MockMarketAPI:
    def get_ticker(self, *args, **kwargs):
        return {"code": "0", "data": [{"last": str(1000.0 if current_price == 0 else current_price)}]}


# -------------------- 限速器 --------------------
class RateLimiter:
    def __init__(self):
        self.last_request_time = 0.0
        self.request_count = 0
        self.window_start = time.time()
        self.max_orders_per_window = 300
        self.window_seconds = 2

    async def check_limit(self, orders_count, max_per_window=None, window_seconds=None):
        max_orders = max_per_window if max_per_window is not None else self.max_orders_per_window
        win = window_seconds if window_seconds is not None else self.window_seconds
        now = time.time()
        elapsed = now - self.window_start
        if elapsed > win:
            self.request_count = 0
            self.window_start = now
            elapsed = 0
        predicted = self.request_count + orders_count
        while predicted > max_orders:
            wait = max(0.0, win - elapsed + 0.05)
            log_action("限速器", f"等待 {wait:.2f}s 避免速率上限", "warning")
            await asyncio.sleep(wait)
            now = time.time()
            elapsed = now - self.window_start
            if elapsed > win:
                self.request_count = 0
                self.window_start = now
                break
            predicted = self.request_count + orders_count
        # small gap between requests
        if now - self.last_request_time < 0.05:
            await asyncio.sleep(max(0.0, 0.05 - (now - self.last_request_time)))
        self.request_count += orders_count
        self.last_request_time = time.time()
        log_action("限速器", f"计数: {self.request_count}/{max_orders}", "debug", {"orders": orders_count})


rate_limiter = RateLimiter()


async def check_rate_limit(n: int, max_per_window: Optional[int] = None, window_seconds: Optional[int] = None):
    await rate_limiter.check_limit(n, max_per_window=max_per_window, window_seconds=window_seconds)


# -------------------- REST：合约 / 价格 / 仓位 / 余额 --------------------
async def fetch_instrument_info_from_api() -> bool:
    """
    Fetch instrument metadata using account_api.get_instruments and update CONTRACT_INFO.
    """
    global CONTRACT_INFO, TICK_SIZE, SYMBOL, INSTRUMENTS_LOADED
    try:
        await check_rate_limit(1, max_per_window=20, window_seconds=2)
        inst_type = CONTRACT_INFO.get("instType", "SWAP")
        log_action("合约信息", f"请求合约信息 instType={inst_type} instId={CONTRACT_INFO.get('symbol')}", "debug")
        try:
            resp = await asyncio.to_thread(account_api.get_instruments, instType=inst_type, instId=CONTRACT_INFO.get("symbol"))
        except TypeError:
            resp = await asyncio.to_thread(account_api.get_instruments, inst_type, CONTRACT_INFO.get("symbol"))
        log_action("合约信息", "收到合约信息响应（原始）", "debug", resp)
        if not isinstance(resp, dict) or str(resp.get("code", "")) != "0" or not resp.get("data"):
            log_action("合约信息", "获取合约信息返回异常或 data 为空", "warning", resp)
            INSTRUMENTS_LOADED = False
            return False
        inst_list = resp.get("data", [])
        target = CONTRACT_INFO.get("symbol", "")
        found = None
        for item in inst_list:
            if item.get("instId") == target:
                found = item
                break
        if not found and target:
            base = target.split("-")[0]
            for item in inst_list:
                iid = item.get("instId", "")
                if iid.startswith(f"{base}-") and "USDT" in iid:
                    found = item
                    break
        if not found:
            log_action("合约信息", f"未找到匹配合约: {target}", "warning", {"returned_count": len(inst_list)})
            INSTRUMENTS_LOADED = False
            return False

        def _parse_float_safe(x, fallback=0.0):
            try:
                if x is None or x == "":
                    return float(fallback)
                return float(x)
            except Exception:
                return float(fallback)

        minSz = _parse_float_safe(found.get("minSz", CONTRACT_INFO.get("minSz", 0)), CONTRACT_INFO.get("minSz", 0))
        tickSz = _parse_float_safe(found.get("tickSz", CONTRACT_INFO.get("tickSz", 0)), CONTRACT_INFO.get("tickSz", 0))
        ctVal = _parse_float_safe(found.get("ctVal", CONTRACT_INFO.get("ctVal", 0)), CONTRACT_INFO.get("ctVal", 0))
        lotSz = _parse_float_safe(found.get("lotSz", CONTRACT_INFO.get("lotSz", 0)), CONTRACT_INFO.get("lotSz", 0))
        ctValCcy = found.get("ctValCcy", CONTRACT_INFO.get("ctValCcy", "ETH"))
        inst_code = found.get("instIdCode", CONTRACT_INFO.get("instIdCode"))
        inst_family = found.get("instFamily", CONTRACT_INFO.get("instFamily"))
        CONTRACT_INFO.update({
            "minSz": minSz,
            "tickSz": tickSz,
            "ctVal": ctVal,
            "lotSz": lotSz,
            "ctValCcy": ctValCcy,
            "instIdCode": inst_code,
            "instFamily": inst_family
        })
        TICK_SIZE = CONTRACT_INFO["tickSz"]
        SYMBOL = CONTRACT_INFO.get("symbol")
        INSTRUMENTS_LOADED = True
        log_action("合约信息", "已更新 CONTRACT_INFO（归一化）", "info", {
            "symbol": SYMBOL,
            "minSz": minSz,
            "tickSz": tickSz,
            "ctVal": ctVal,
            "lotSz": lotSz,
            "ctValCcy": ctValCcy,
            "instIdCode": inst_code,
            "instFamily": inst_family
        })
        return True
    except Exception as e:
        INSTRUMENTS_LOADED = False
        log_action("合约信息", f"获取合约信息异常: {e}", "error", exc_info=True)
        return False


async def update_current_price() -> bool:
    """
    Query market ticker via REST and update current_price.
    """
    global current_price, last_price, last_api_price_update, price_source
    try:
        await check_rate_limit(1)
        log_action("价格查询", "请求 ticker", "debug")
        try:
            resp = await asyncio.to_thread(market_api.get_ticker, instId=SYMBOL)
        except TypeError:
            resp = await asyncio.to_thread(market_api.get_ticker, SYMBOL)
        log_action("价格查询", "收到响应", "debug", resp)
        if isinstance(resp, dict) and str(resp.get("code", "")) in ("0", 0) and resp.get("data"):
            data0 = resp["data"][0]
            price = None
            for key in ("last", "lastPx", "price", "c", "close"):
                if key in data0:
                    price = safe_float(data0.get(key, 0), 0.0)
                    break
            if price is None:
                log_action("价格查询", "无法解析 ticker 返回中的价格字段", "warning", data0)
                return False
            last_price = current_price
            current_price = price
            last_api_price_update = time.time()
            price_source = "rest_api"
            log_action("API价格更新", f"${last_price:.4f} -> ${price:.4f}", "info")
            return True
    except Exception as e:
        log_action("价格查询", f"异常: {e}", "error", exc_info=True)
    return False


async def update_position_info() -> bool:
    """
    Query positions via REST and update position_info.
    """
    global position_info
    try:
        await check_rate_limit(1)
        log_action("仓位查询", "发送仓位查询请求", "debug")
        try:
            resp = await asyncio.to_thread(account_api.get_positions, instType=CONTRACT_INFO.get("instType", "SWAP"), instId=CONTRACT_INFO.get("symbol"))
        except TypeError:
            resp = await asyncio.to_thread(account_api.get_positions, CONTRACT_INFO.get("instType", "SWAP"), CONTRACT_INFO.get("symbol"))
        log_action("仓位查询", "收到仓位查询响应", "debug", resp)
        if not isinstance(resp, dict) or str(resp.get("code", "")) not in ("0", 0) or not resp.get("data"):
            log_action("仓位查询", "仓位查询返回非 0 或空响应", "warning", resp)
            return False
        # reset only fields; keep mapping keys
        for key in list(position_info.keys()):
            position_info[key].update({"pos": 0.0, "usdt_value": 0.0, "avg_px": 0.0, "upl": 0.0})
        data = resp.get("data", [])
        for entry in data:
            if not isinstance(entry, dict):
                continue
            inst_id = entry.get("instId") or CONTRACT_INFO.get("symbol")
            pos_raw = entry.get("pos", entry.get("position", "0"))
            pos = safe_float(pos_raw, 0.0)
            pos_side = (entry.get("posSide") or "net").lower()
            # determine logical side and absolute size
            if pos_side == "net":
                if pos < 0:
                    side = "short"
                    size = abs(pos)
                else:
                    side = "long"
                    size = pos
            elif pos_side in ("long", "short"):
                side = pos_side
                size = abs(pos)
            else:
                side = "net"
                size = pos
            # try to get markPx or last to compute notional in quote currency (USDT)
            mark_px = safe_float(entry.get("markPx") or entry.get("last") or 0.0, 0.0)
            usdt_value = 0.0
            if mark_px and CONTRACT_INFO.get("ctVal"):
                usdt_value = float(Decimal(str(size)) * Decimal(str(CONTRACT_INFO.get("ctVal", 0))) * Decimal(str(mark_px)))
            else:
                # fallback using reported notionalUsd if present
                usdt_value = safe_float(entry.get("notionalUsd", 0.0), 0.0)
            pk = f"{inst_id}-{side}"
            position_info[pk]["pos"] = size
            position_info[pk]["usdt_value"] = usdt_value
            position_info[pk]["avg_px"] = safe_float(entry.get("avgPx", 0.0))
            position_info[pk]["upl"] = safe_float(entry.get("upl", 0.0))
            position_info[pk]["entry_time"] = int(time.time())
            position_info[pk]["meta"] = {
                "posSide_raw": entry.get("posSide"),
                "posId": entry.get("posId"),
                "instType": entry.get("instType"),
                "markPx": mark_px,
                "lever": entry.get("lever")
            }
            log_action("仓位更新", f"{inst_id} {side} {size} 张 -> {usdt_value:.6f} USDT", "debug", position_info[pk])
        return True
    except Exception as e:
        log_action("仓位查询", f"请求失败: {e}", "error", exc_info=True)
        return False


async def fetch_account_balance() -> bool:
    """
    Fetch account balances and convert all currencies to USDT-equivalent.
    """
    global account_equity_usdt, initial_equity_usdt
    try:
        await check_rate_limit(1)
        log_action("账户查询", "发送账户余额请求", "debug")
        try:
            resp = await asyncio.to_thread(account_api.get_account_balance, ccy="")
        except TypeError:
            resp = await asyncio.to_thread(account_api.get_account_balance, "")
        log_action("账户查询", "收到账户余额响应", "debug", resp)
        if not isinstance(resp, dict) or str(resp.get("code", "")) not in ("0", 0) or not resp.get("data"):
            log_action("账户查询", "账户返回异常或 data 为空", "warning", resp)
            return False
        total_usdt = Decimal("0")
        balances = {}
        # data is a list: each item has 'details' list with {ccy, availEq, eq, cashBal, frozenBal, ...}
        for grp in resp.get("data", []):
            details = grp.get("details") or grp.get("details", [])
            for d in details:
                ccy = d.get("ccy") or d.get("currency") or ""
                # many API variants use 'eq' for total equity in that currency
                eq = safe_float(d.get("eq", d.get("cashBal", d.get("availEq", 0.0))), 0.0)
                balances[ccy] = eq
        # convert each currency to USDT
        for ccy, eq in balances.items():
            if ccy.upper() == "USDT":
                total_usdt += Decimal(str(eq))
                continue
            # Try to find a ticker to convert ccy -> USDT
            price = None
            candidates = [
                f"{ccy}-USDT",
                f"{ccy}-USDT-SWAP",
                f"{ccy}-USDT-SWAP".replace("--", "-"),
                f"{ccy}-USD",
                f"{ccy}-USD-SWAP"
            ]
            for cand in candidates:
                try:
                    try:
                        tresp = await asyncio.to_thread(market_api.get_ticker, instId=cand)
                    except TypeError:
                        tresp = await asyncio.to_thread(market_api.get_ticker, cand)
                    if isinstance(tresp, dict) and str(tresp.get("code", "")) in ("0", 0) and tresp.get("data"):
                        data0 = tresp["data"][0]
                        for k in ("last", "lastPx", "price", "c", "close"):
                            if k in data0:
                                price = safe_float(data0.get(k, 0), None)
                                break
                        if price is not None and price > 0:
                            log_action("余额转换", f"使用 {cand} 的价格 {price:.6f} 将 {eq} {ccy} 转换为 USDT", "debug")
                            break
                except Exception:
                    price = None
            if price is None:
                log_action("余额转换", f"无法找到 {ccy} -> USDT 的市场价格，跳过该币种的折算（视为 0）", "warning", {"ccy": ccy})
                continue
            converted = Decimal(str(eq)) * Decimal(str(price))
            total_usdt += converted
        account_equity_usdt = float(total_usdt)
        if initial_equity_usdt == 0.0:
            initial_equity_usdt = account_equity_usdt
            log_action("账户初始化", f"初始权益 (USDT): {initial_equity_usdt:.2f}", "info")
        else:
            log_action("账户更新", f"账户余额 (USDT): {account_equity_usdt:.2f}", "debug", {"balances": balances})
        return True
    except Exception as e:
        log_action("账户查询", f"异常: {e}", "error", exc_info=True)
        return False


# (file truncated for brevity in tool call)