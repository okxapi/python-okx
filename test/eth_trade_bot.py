#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETH perpetual trading bot for OKX.

Key behavior for this version:
- On initialization, loads instrument metadata (via REST) and initial account balances (via REST).
- All account balances are converted/aggregated into USDT-equivalent and stored in `account_equity_usdt`.
- During continuous run, websocket (private) subscriptions update positions and balances in real-time.
- REST calls are wrapped with asyncio.to_thread to avoid blocking the event loop.
- Uses Decimal where needed for numeric precision on sizes and prices.
- Supports a mock mode (USE_MOCK=1) for offline testing.

How to use:
- Set OKX API credentials through environment variables:
  OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE
- Ensure OKX_FLAG=1 for testnet/simulated trading or 0 for live (use testnet keys for safety).
- Run: python test/eth_trade_bot.py
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
from typing import Optional, Dict, Any

# Optional imports (OKX SDK). If not installed and USE_MOCK=1, script will use mock APIs.
try:
    from okx.websocket.WsPrivateAsync import WsPrivateAsync as PrivateWs
    import okx.Account as Account
    import okx.Trade as Trade
    import okx.MarketData as MarketData
except Exception:
    PrivateWs = None
    Account = None
    Trade = None
    MarketData = None

getcontext().prec = 28

# -------------------- Config & Defaults --------------------
USE_MOCK = os.getenv("USE_MOCK", "0") == "1"

API_KEY = os.getenv("OKX_API_KEY", "")
SECRET_KEY = os.getenv("OKX_SECRET_KEY", "")
PASSPHRASE = os.getenv("OKX_PASSPHRASE", "")

OKX_FLAG = os.getenv("OKX_FLAG", "1")  # "1" testnet, "0" live

RUN_FOREVER = True
RUN_SIMULATOR = False

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

# -------------------- Logging --------------------
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


# -------------------- Global runtime state --------------------
# account_equity_usdt: total account cash balances converted to USDT
account_equity_usdt: float = 0.0
# initial equity (USDT) at startup
initial_equity_usdt: float = 0.0

# current price used for strategy (quote currency)
current_price: float = 0.0
last_price: float = 0.0
price_source: str = "unknown"
last_ws_price_update: float = 0.0
last_api_price_update: float = 0.0

trading_direction = TRADE_STRATEGY.get("fixed_trend_direction", "long")
INSTRUMENTS_LOADED = False

# orders / positions
active_orders: Dict[str, dict] = {}
order_pair_mapping: Dict[str, dict] = {}
position_info = defaultdict(lambda: {"pos": 0.0, "usdt_value": 0.0, "avg_px": 0.0, "upl": 0.0, "entry_time": 0})

# API clients (populated in initialize_clients)
account_api = None
trade_api = None
market_api = None

# ws instance holder for cleanup
_ws_instance = None

# -------------------- Utils --------------------
def safe_float(v, default: float = 0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def generate_order_id(prefix: str) -> str:
    clean = ''.join(c for c in prefix if c.isalnum())
    return (clean + ''.join(random.choices(string.ascii_letters + string.digits, k=16)))[:32]


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


def calculate_contract_value_from_contracts(contracts: float, price: float) -> float:
    """
    Given number of contracts (contracts), CTVAL (CONTRACT_INFO['ctVal']) and price,
    compute USDT notional: contracts * ctVal * price.
    """
    ct = CONTRACT_INFO.get("ctVal", 0) or 0
    try:
        return float(Decimal(str(contracts)) * Decimal(str(ct)) * Decimal(str(price)))
    except Exception:
        return 0.0


# -------------------- Mock APIs --------------------
class MockTradeAPI:
    def place_order(self, **kwargs):
        return {"code": "0", "data": [{"ordId": f"mock_{int(time.time() * 1000)}", "clOrdId": kwargs.get("clOrdId", "")}]}

    def place_multiple_orders(self, batch):
        return {"code": "0", "data": [{"clOrdId": r["clOrdId"], "sCode": "0", "ordId": f"mock_{random.randint(1000, 9999)}"} for r in batch]}

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
        return {
            "code": "0",
            "data": [
                {
                    "instId": CONTRACT_INFO["symbol"],
                    "minSz": "0.01",
                    "tickSz": "0.01",
                    "ctVal": "0.1",
                    "lotSz": "0.01",
                    "ctValCcy": "ETH",
                    "instIdCode": "2021032601102994",
                    "instFamily": "ETH-USDT"
                }
            ]
        }


class MockMarketAPI:
    def get_ticker(self, *args, **kwargs):
        # return last for symbol
        return {"code": "0", "data": [{"last": str(1000.0 if current_price == 0 else current_price)}]}


# -------------------- Rate limiter --------------------
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


# -------------------- REST: instruments / price / positions / balance --------------------
async def fetch_instrument_info_from_api() -> bool:
    """
    Fetch instrument metadata using account_api.get_instruments and update CONTRACT_INFO.
    Must be called before trading.
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
    Accepts different field names returned by SDK (last, lastPx, c, close).
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
    Query positions via REST and update position_info. Also compute USDT notional per position if possible.
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
                usdt_value = calculate_contract_value_from_contracts(size, mark_px)
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
    Sets account_equity_usdt and initial_equity_usdt on first success.
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
            # try common ticker symbol patterns
            candidates = [
                f"{ccy}-USDT",
                f"{ccy}-USDT-SWAP",
                f"{ccy}-USDT-SWAP".replace("--", "-"),
                f"{ccy}-USD",
                f"{ccy}-USD-SWAP"
            ]
            for cand in candidates:
                try:
                    # call market_api.get_ticker
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
                    # ignore and try next candidate
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


# -------------------- Orders (place/cancel) --------------------
async def cancel_single_order(cl_ord_id: str) -> bool:
    try:
        await check_rate_limit(1)
        req = {"instId": SYMBOL, "clOrdId": cl_ord_id}
        resp = await asyncio.to_thread(trade_api.cancel_order, **req)
        log_action("取消订单", f"{cl_ord_id} -> {resp.get('code')}", "debug", resp)
        if str(resp.get("code", "")) in ("0", 0) and cl_ord_id in active_orders:
            del active_orders[cl_ord_id]
            return True
        return False
    except Exception as e:
        log_action("取消订单", f"异常: {e}", "error", exc_info=True)
        return False


async def place_order_simple(side: str, pos_side: str, ord_type: str, sz: str, px: Optional[str] = None, reduce_only: bool = False) -> dict:
    """
    Helper to place a single order. Returns resp dict.
    """
    cl = generate_order_id("ORD")
    req = {"instId": SYMBOL, "tdMode": "isolated", "clOrdId": cl, "side": side, "posSide": pos_side, "ordType": ord_type, "sz": str(sz)}
    if px is not None:
        req["px"] = str(px)
    if reduce_only:
        req["reduceOnly"] = True
    try:
        await check_rate_limit(1)
        resp = await asyncio.to_thread(trade_api.place_order, **req)
        log_action("下单", "响应", "debug", resp)
        if str(resp.get("code", "")) in ("0", 0):
            # record
            ord_id = resp.get("data", [{}])[0].get("ordId", "")
            active_orders[cl] = {"ord_id": ord_id, "cl": cl, "px": px, "sz": sz, "state": "live", "type": ord_type, "create_time": time.time()}
        return resp
    except Exception as e:
        log_action("下单", f"异常: {e}", "error", exc_info=True)
        return {"code": "-1", "msg": str(e)}


# -------------------- WebSocket integration (positions + balance_and_position) --------------------
def _handle_positions_ws_entry(entry: Dict[str, Any]):
    """Synchronous callback for WS messages to update position_info."""
    try:
        inst_id = entry.get("instId")
        pos_raw = entry.get("pos", "0")
        pos = safe_float(pos_raw, 0.0)
        pos_side = (entry.get("posSide") or "net").lower()
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
        mark_px = safe_float(entry.get("markPx") or entry.get("last") or 0.0, 0.0)
        usdt_value = 0.0
        if mark_px and CONTRACT_INFO.get("ctVal"):
            usdt_value = calculate_contract_value_from_contracts(size, mark_px)
        else:
            usdt_value = safe_float(entry.get("notionalUsd", 0.0), 0.0)
        pk = f"{inst_id}-{side}"
        position_info[pk]["pos"] = size
        position_info[pk]["usdt_value"] = usdt_value
        position_info[pk]["avg_px"] = safe_float(entry.get("avgPx", 0.0))
        position_info[pk]["upl"] = safe_float(entry.get("upl", 0.0))
        position_info[pk]["entry_time"] = int(time.time())
        log_action("WS仓位", f"{inst_id} {side} {size} -> {usdt_value:.6f}USDT", "debug", position_info[pk])
    except Exception as e:
        log_action("WS仓位处理", f"错误: {e}", "error", exc_info=True)


def _handle_balance_and_position_ws_entry(entry: Dict[str, Any]):
    """Update account_equity_usdt from balance_and_position snapshot/event."""
    global account_equity_usdt, initial_equity_usdt, last_ws_price_update
    try:
        # update balances
        bal_data = entry.get("balData", []) or entry.get("bal", [])
        if isinstance(bal_data, dict):
            bal_data = [bal_data]
        total_usdt = Decimal("0")
        for b in bal_data:
            ccy = b.get("ccy")
            eq = safe_float(b.get("cashBal", b.get("eq", 0.0)), 0.0)
            if ccy and ccy.upper() == "USDT":
                total_usdt += Decimal(str(eq))
            else:
                # try to convert via REST ticker (synchronous here: prefer async path; but WS callback might be sync)
                # We'll attempt a simple non-blocking best-effort (don't block event loop)
                price = None
                try:
                    # attempt known tickers quickly using market_api (this may be blocking if not thread-wrapped,
                    # but WS callbacks in this SDK are often called in background threads; we'll best-effort)
                    tresp = None
                    try:
                        tresp = market_api.get_ticker(instId=f"{ccy}-USDT")
                    except Exception:
                        try:
                            tresp = market_api.get_ticker(f"{ccy}-USDT")
                        except Exception:
                            tresp = None
                    if isinstance(tresp, dict) and tresp.get("data"):
                        data0 = tresp["data"][0]
                        for k in ("last", "lastPx", "price", "c", "close"):
                            if k in data0:
                                price = safe_float(data0.get(k, 0.0), 0.0)
                                break
                except Exception:
                    price = None
                if price and price > 0:
                    total_usdt += Decimal(str(eq)) * Decimal(str(price))
                else:
                    log_action("WS余额转换", f"无法在 WS 回调中转换 {ccy} -> USDT（视为 0）", "warning", {"ccy": ccy})
        account_equity_usdt = float(total_usdt)
        if initial_equity_usdt == 0.0:
            initial_equity_usdt = account_equity_usdt
        last_ws_price_update = time.time()
        log_action("WS余额更新", f"账户余额 (USDT): {account_equity_usdt:.2f}", "debug")
    except Exception as e:
        log_action("WS balance处理", f"异常: {e}", "error", exc_info=True)


def _ws_message_callback(message: Any):
    """General WS message callback. SDK may call this synchronously."""
    try:
        data = message
        if isinstance(message, str):
            try:
                data = json.loads(message)
            except Exception:
                log_action("WS消息", "收到非 JSON 字符串消息", "debug", {"raw": message})
                return
        # handle subscription events
        if "event" in data:
            ev = data.get("event")
            log_action("WS事件", f"event={{ev}}", "debug", data)
            return
        arg = data.get("arg") or {}
        channel = arg.get("channel") or data.get("channel")
        if channel in ("positions", "balance_and_position"):
            payload_list = data.get("data", [])
            if isinstance(payload_list, dict):
                payload_list = [payload_list]
            for payload in payload_list:
                if channel == "positions":
                    # payload may be list in snapshot
                    if isinstance(payload, list):
                        for it in payload:
                            _handle_positions_ws_entry(it)
                    else:
                        _handle_positions_ws_entry(payload)
                else:
                    _handle_balance_and_position_ws_entry(payload)
        else:
            log_action("WS消息", "未知频道消息", "debug", data)
    except Exception as e:
        log_action("WS回调", f"处理消息异常: {e}", "error", exc_info=True)


async def start_private_ws():
    """Start private websocket client and subscribe to positions & balance_and_position."""
    global _ws_instance
    if PrivateWs is None:
        log_action("WS", "WsPrivateAsync 不可用（SDK 未安装），跳过 WS 订阅", "warning")
        return None
    try:
        ws = PrivateWs(apiKey=API_KEY, passphrase=PASSPHRASE, secretKey=SECRET_KEY, url="wss://ws.okx.com:8443/ws/v5/private", useServerTime=False)
        await ws.start()
        _ws_instance = ws
        log_action("WS", "私有 WS 已启动", "info")
        args = [
            {"channel": "positions", "instType": "ANY"},
            {"channel": "balance_and_position"}
        ]
        await ws.subscribe(args, callback=_ws_message_callback)
        log_action("WS", "已订阅 positions 与 balance_and_position", "info", {"sub_args": args})
        return ws
    except Exception as e:
        log_action("WS启动", f"启动或订阅失败: {e}", "error", exc_info=True)
        return None


async def stop_private_ws():
    global _ws_instance
    try:
        if _ws_instance is None:
            return
        try:
            await _ws_instance.stop()
        except Exception:
            pass
        _ws_instance = None
        log_action("WS", "私有 WS 已停止", "info")
    except Exception as e:
        log_action("WS停止", f"停止失败: {e}", "warning", exc_info=True)


# -------------------- Main loop --------------------
def log_periodic_status():
    long_key = f"{CONTRACT_INFO.get('symbol')}-long"
    short_key = f"{CONTRACT_INFO.get('symbol')}-short"
    long_pos = position_info[long_key]["pos"] if long_key in position_info else 0.0
    short_pos = position_info[short_key]["pos"] if short_key in position_info else 0.0
    logger.info("\n" + "=" * 80)
    logger.info(f"📊 状态 - 方向: {trading_direction} - 多: {long_pos} - 空: {short_pos} - 余额(USDT): {account_equity_usdt:.2f}")
    logger.info("=" * 80 + "\n")


async def main_loop_once():
    # initialization steps: ensure instrument metadata and initial balances loaded
    if not INSTRUMENTS_LOADED:
        ok = await fetch_instrument_info_from_api()
        if not ok:
            log_action("主流程", "未能加载合约元数据，进入 Dry-run 模式（不会下单）", "warning")
            # still attempt to refresh price and balances for visibility
            await update_current_price()
            await fetch_account_balance()
            await update_position_info()
            log_periodic_status()
            return
        await update_current_price()
        await fetch_account_balance()
        await update_position_info()
        # trading decision simplified: if no active orders, try to place a pair
        if not active_orders:
            log_action("主流程", "无活跃订单（或仅观测模式），当前不会主动下单（策略留空）", "info")
        log_periodic_status()


async def main_loop_continuous():
    # start ws if not mock and PrivateWs available
    ws_task = None
    if not USE_MOCK and PrivateWs is not None:
        ws_task = asyncio.create_task(start_private_ws())
    try:
        while True:
            try:
                await main_loop_once()
            except Exception as e:
                log_action("主循环", f"异常: {e}", "error", exc_info=True)
            await asyncio.sleep(5)
    finally:
        if ws_task:
            try:
                await stop_private_ws()
            except Exception:
                pass


# -------------------- Initialization --------------------
def initialize_clients():
    global account_api, trade_api, market_api
    if USE_MOCK:
        account_api = MockAccountAPI()
        trade_api = MockTradeAPI()
        market_api = MockMarketAPI()
        log_action("初始化", "使用 Mock APIs (USE_MOCK=1)", "info")
    else:
        if Account is None or Trade is None or MarketData is None:
            log_action("初始化", "OKX SDK 未安装且 USE_MOCK=False，无法继续", "error")
            raise RuntimeError("OKX SDK not installed; set USE_MOCK=1 to run mock mode")
        account_api = Account.AccountAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
        trade_api = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
        market_api = MarketData.MarketAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
        log_action("初始化", f"已初始化 OKX SDK (flag={OKX_FLAG})", "info")


# -------------------- Entrypoint --------------------
if __name__ == "__main__":
    initialize_clients()
    log_action("程序启动", f"模式: OKX_FLAG={OKX_FLAG}, USE_MOCK={USE_MOCK}", "info")
    if RUN_FOREVER:
        asyncio.run(main_loop_continuous())
    else:
        asyncio.run(main_loop_once())