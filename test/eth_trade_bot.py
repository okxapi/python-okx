#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETH perpetual trading bot for OKX (SDK-only, testnet-ready).

Security:
- Do NOT hard-code API keys into source files.
- This script reads credentials from environment variables:
    OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE, OKX_FLAG
- For quick local testing, export/set these env vars in your shell before running.

This file includes:
 - SDK init (Account/Trade/MarketData, PrivateWs/PublicWs)
 - REST helpers (fetch instrument, balances, positions, orders)
 - WebSocket handling (private channels: account, orders, fills, positions, balance_and_position; public: tickers)
 - Strategy helpers: continuous-eaten protection, gatekeeper, dynamic offset, place_pair_if_ok
"""

import asyncio
import time
import json
import logging
import random
import os
import sys
from datetime import datetime, timezone
from collections import defaultdict, deque
from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Optional, Dict, Any, List
import math

# ---------------- Credentials (from environment) ----------------
# API_KEY = os.getenv("OKX_API_KEY", "")
# SECRET_KEY = os.getenv("OKX_SECRET_KEY", "")
# PASSPHRASE = os.getenv("OKX_PASSPHRASE", "")
# OKX_FLAG = os.getenv("OKX_FLAG", "1")  # "1" for testnet, "0" for mainnet

API_KEY = os.getenv("OKX_API_KEY", "52c6b3db-8827-477d-8e25-9c8b14d816e7")
SECRET_KEY = os.getenv("OKX_SECRET_KEY", "6AA11170CBC857418B3FEA38127703CA")
PASSPHRASE = os.getenv("OKX_PASSPHRASE", "Jinquan169..")
OKX_FLAG = os.getenv("OKX_FLAG", "1")  # "1" for testnet, "0" for mainnet

# ---------------- SDK imports ----------------
try:
    from okx.websocket.WsPrivateAsync import WsPrivateAsync as PrivateWs
    from okx.websocket.WsPublicAsync import WsPublicAsync as PublicWs
    import okx.Account as Account
    import okx.Trade as Trade
    import okx.MarketData as MarketData
except Exception:
    PrivateWs = None
    PublicWs = None
    Account = None
    Trade = None
    MarketData = None

getcontext().prec = 28

# ---------------- Logging ----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "trading.log")

logger = logging.getLogger("eth_trade_bot")
logger.setLevel(logging.DEBUG)
for h in list(logger.handlers):
    logger.removeHandler(h)
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)
try:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
except Exception:
    pass
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(ch)


def log_action(action: str, details: str, level: str = "info", extra: Optional[dict] = None, exc_info: bool = False):
    prefix = {
        "debug": "🔵",
        "info": "🟢",
        "warning": "🟠",
        "error": "🔴",
        "critical": "⛔"
    }.get(level, "⚪")
    ts = datetime.now(timezone.utc).isoformat()
    msg = f"[{ts}] {prefix} {action} - {details}"
    if extra:
        try:
            msg += " | " + json.dumps(extra, ensure_ascii=False)
        except Exception:
            msg += f" | {extra}"
    try:
        if level == "debug":
            logger.debug(msg, exc_info=exc_info)
        elif level == "warning":
            logger.warning(msg, exc_info=exc_info)
        elif level == "error":
            logger.error(msg, exc_info=exc_info)
        elif level == "critical":
            logger.critical(msg, exc_info=exc_info)
        else:
            logger.info(msg, exc_info=exc_info)
    except UnicodeEncodeError:
        safe_msg = msg.encode("utf-8", errors="replace").decode("utf-8")
        if level == "debug":
            logger.debug(safe_msg, exc_info=exc_info)
        elif level == "warning":
            logger.warning(safe_msg, exc_info=exc_info)
        elif level == "error":
            logger.error(safe_msg, exc_info=exc_info)
        elif level == "critical":
            logger.critical(safe_msg, exc_info=exc_info)
        else:
            logger.info(safe_msg, exc_info=exc_info)

# ---------------- Globals & Config ----------------
SYMBOL = "ETH-USDT-SWAP"
CONTRACT_INFO: Dict[str, Any] = {"symbol": SYMBOL, "minSz": 0.0, "tickSz": 0.0, "ctVal": 0.0, "ctValCcy": "ETH", "instType": "SWAP"}
TICK_SIZE = CONTRACT_INFO["tickSz"]

STRATEGY = {
    "base_notional_fraction": 0.25,
    "leverage": 5,
    "price_offset": 0.001,
    "expected_hold_seconds": 300,
    "expected_slippage_pct": 0.0002,
    "order_type": "limit"
}

# Runtime state
account_equity_usdt = 0.0
initial_equity_usdt = 0.0
current_price = 0.0
last_price = 0.0
price_source = "unknown"

active_orders: Dict[str, dict] = {}
position_info = defaultdict(lambda: {"pos": 0.0, "avg_px": 0.0, "usdt_value": 0.0})

# pairs & lock
active_pairs: Dict[str, dict] = {}
orders_lock = asyncio.Lock()

# SDK clients
account_api = None
trade_api = None
market_api = None

# WS instances
_ws_instance = None
_public_ws_instance = None

# Dedup sets
seen_trade_ids = set()
seen_filled_ordids = set()
seen_reqids = set()

# Public ticker best bid/ask
best_bid = 0.0
best_ask = 0.0

# Controls
ENABLE_FILLS_CHANNEL = False
ENABLE_PUBLIC_TICKER = True

# ---------------- Utilities ----------------
def safe_float(v, default=0.0):
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def generate_order_id(prefix: str = "o"):
    suffix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    ts = int(time.time() * 1000) % 1000000
    return f"{prefix}{ts}{suffix}"[:32]


def round_price_by_tick(p: float, tick: float):
    try:
        if tick <= 0:
            return p
        q = Decimal(str(p)) / Decimal(str(tick))
        qr = q.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        return float((qr * Decimal(str(tick))).normalize())
    except Exception:
        return p


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


# ---------------- Rate limiter ----------------
class RateLimiter:
    def __init__(self):
        self.window_start = time.time()
        self.count = 0
        self.window_seconds = 2
        self.max_per_window = 300
        self.last_request_time = 0.0

    async def wait_for(self, n=1, max_per_window=None, window_seconds=None):
        max_w = max_per_window if max_per_window is not None else self.max_per_window
        win = window_seconds if window_seconds is not None else self.window_seconds
        while True:
            now = time.time()
            if now - self.window_start >= win:
                self.window_start = now
                self.count = 0
            if self.count + n <= max_w:
                if now - self.last_request_time < 0.05:
                    await asyncio.sleep(max(0.0, 0.05 - (now - self.last_request_time)))
                self.count += n
                self.last_request_time = time.time()
                return
            await asyncio.sleep(0.05)


rate_limiter = RateLimiter()

# ---------------- Initialization ----------------
def initialize_clients():
    global account_api, trade_api, market_api
    if Account is None or Trade is None or MarketData is None:
        log_action("初始化", "OKX SDK 未安装，请 pip install python-okx", "error")
        raise RuntimeError("OKX SDK not installed")
    account_api = Account.AccountAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
    trade_api = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
    market_api = MarketData.MarketAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
    log_action("初始化", f"OKX SDK 已初始化 (flag={OKX_FLAG})", "info")


# ---------------- REST helpers ----------------
async def fetch_instrument_info():
    global CONTRACT_INFO, TICK_SIZE, SYMBOL
    await rate_limiter.wait_for(1, max_per_window=20, window_seconds=2)
    try:
        resp = await asyncio.to_thread(account_api.get_instruments, instType=CONTRACT_INFO.get("instType", "SWAP"), instId=SYMBOL)
    except TypeError:
        resp = await asyncio.to_thread(account_api.get_instruments, CONTRACT_INFO.get("instType", "SWAP"), SYMBOL)
    log_action("合约", "拿到合约信息", "debug", {"resp_code": resp.get("code") if isinstance(resp, dict) else None})
    if not isinstance(resp, dict) or str(resp.get("code", "")) != "0" or not resp.get("data"):
        log_action("合约", "获取合约信息失败", "warning", resp)
        return False
    data = resp.get("data", [])
    found = None
    for it in data:
        if it.get("instId") == SYMBOL:
            found = it
            break
    if not found:
        for it in data:
            if it.get("instId", "").startswith(SYMBOL.split("-")[0]) and "USDT" in it.get("instId", ""):
                found = it
                break
    if not found:
        log_action("合约", "没有找到合约信息", "error", {"symbol": SYMBOL})
        return False
    CONTRACT_INFO["minSz"] = safe_float(found.get("minSz", CONTRACT_INFO.get("minSz", 0)))
    CONTRACT_INFO["tickSz"] = safe_float(found.get("tickSz", CONTRACT_INFO.get("tickSz", 0)))
    CONTRACT_INFO["ctVal"] = safe_float(found.get("ctVal", CONTRACT_INFO.get("ctVal", 0)))
    CONTRACT_INFO["ctValCcy"] = found.get("ctValCcy", CONTRACT_INFO.get("ctValCcy"))
    TICK_SIZE = CONTRACT_INFO["tickSz"]
    log_action("合约", "合约信息更新成功", "info", CONTRACT_INFO)
    return True


async def update_price_from_rest():
    global current_price, last_price, price_source
    await rate_limiter.wait_for(1)
    try:
        resp = await asyncio.to_thread(market_api.get_ticker, instId=SYMBOL)
    except TypeError:
        resp = await asyncio.to_thread(market_api.get_ticker, SYMBOL)
    if isinstance(resp, dict) and str(resp.get("code", "")) in ("0", 0) and resp.get("data"):
        d = resp["data"][0]
        p = None
        for k in ("last", "lastPx", "price"):
            if k in d:
                p = safe_float(d.get(k))
                break
        if p is not None:
            last_price = current_price
            current_price = p
            price_source = "rest"
            log_action("价格", f"REST 价格更新 {current_price}", "debug")
            return True
    return False


async def fetch_account_and_positions():
    global account_equity_usdt, initial_equity_usdt
    await rate_limiter.wait_for(1)
    try:
        resp = await asyncio.to_thread(account_api.get_account_balance, ccy="")
    except TypeError:
        resp = await asyncio.to_thread(account_api.get_account_balance, "")
    log_action("账户", "余额获取（简略）", "debug")
    try:
        if isinstance(resp, dict) and resp.get("data"):
            total = 0
            for grp in resp.get("data", []):
                for d in grp.get("details", []) if grp.get("details") else []:
                    if (d.get("ccy") or d.get("currency") or "").upper() == "USDT":
                        total += safe_float(d.get("eq", d.get("availEq", 0)), 0.0)
            if total > 0:
                account_equity_usdt = float(total)
                if initial_equity_usdt == 0.0:
                    initial_equity_usdt = account_equity_usdt
    except Exception:
        pass
    try:
        resp2 = await asyncio.to_thread(account_api.get_positions, instType=CONTRACT_INFO.get("instType", "SWAP"), instId=SYMBOL)
        log_action("仓位", "仓位查询返回（简略）", "debug", resp2)
    except Exception:
        pass


# ---------------- Order helpers ----------------
async def place_order_simple(side: str, pos_side: str, ord_type: str, sz: str, px: Optional[str] = None, cl_ord_id: Optional[str] = None):
    cl = cl_ord_id or generate_order_id("cl")
    try:
        szf = float(sz)
    except Exception:
        szf = float(sz)
    minsz = CONTRACT_INFO.get("minSz", 0) or 0.0
    if minsz > 0 and szf < minsz:
        szf = minsz
    sz_str = str(szf)
    px_str = None
    if px is not None:
        px_str = str(round_price_by_tick(float(px), CONTRACT_INFO.get("tickSz", 0.0)))
    req = {"instId": SYMBOL, "tdMode": "isolated", "clOrdId": cl, "side": side, "ordType": ord_type, "sz": sz_str}
    if pos_side:
        req["posSide"] = pos_side
    if px_str:
        req["px"] = px_str
    await rate_limiter.wait_for(1, max_per_window=60, window_seconds=2)
    try:
        resp = await asyncio.to_thread(trade_api.place_order, **req)
    except Exception as e:
        log_action("下单", f"下单异常: {e}", "error", exc_info=True)
        prev = active_orders.get(cl, {})
        prev.update({"ord_id": "", "cl": cl, "px": px_str, "sz": sz_str, "state": "error", "raw": str(e)})
        active_orders[cl] = prev
        return {"code": "-1", "msg": str(e)}
    if isinstance(resp, dict):
        data0 = (resp.get("data") or [{}])[0]
        ord_id = data0.get("ordId") or ""
        prev = active_orders.get(cl, {})
        prev.update({"ord_id": ord_id, "cl": cl, "px": px_str, "sz": sz_str, "state": "accepted", "raw": data0})
        active_orders[cl] = prev
    else:
        prev = active_orders.get(cl, {})
        prev.update({"ord_id": "", "cl": cl, "px": px_str, "sz": sz_str, "state": "unknown", "raw": resp})
        active_orders[cl] = prev
    log_action("下单", f"已提交订单 cl={cl}", "info", resp)
    return resp


async def cancel_order_by_cl(cl: str):
    await rate_limiter.wait_for(1, max_per_window=60, window_seconds=2)
    try:
        resp = await asyncio.to_thread(trade_api.cancel_order, instId=SYMBOL, clOrdId=cl)
        log_action("撤单", f"撤单请求提交 cl={cl}", "info", resp)
        return resp
    except Exception as e:
        log_action("撤单", f"撤单异常: {e}", "error", exc_info=True)
        return {"code": "-1", "msg": str(e)}


# ---------------- Helper: find other cl in same pair ----------------
def get_other_cl_of_active_pair(cl: str) -> Optional[str]:
    """
    From active_pairs mapping return the other cl in the same pair, or None.
    """
    try:
        for pid, p in active_pairs.items():
            buy = p.get("buy") or {}
            sell = p.get("sell") or {}
            if buy.get("cl") == cl:
                return sell.get("cl")
            if sell.get("cl") == cl:
                return buy.get("cl")
    except Exception:
        return None
    return None


# ---------------- Exposure helper ----------------
def net_exposure_exceeds_threshold(threshold_fraction: float = 0.3) -> bool:
    """
    Compute an approximate net exposure in USDT and check if it exceeds threshold_fraction of equity.
    Uses position_info[*]['usdt_value'] when available, otherwise estimates as pos*avg_px*ctVal.
    """
    try:
        equity = float(account_equity_usdt or 0.0)
        if equity <= 0:
            return False
        net = 0.0
        for k, v in position_info.items():
            usdt_val = v.get("usdt_value", None)
            if usdt_val is None:
                pos = safe_float(v.get("pos", 0.0))
                avg_px = safe_float(v.get("avg_px", current_price or 0.0))
                ct = safe_float(v.get("ctVal", CONTRACT_INFO.get("ctVal", 1.0)))
                est = pos * avg_px * (ct or 1.0)
                usdt_val = est
            net += safe_float(usdt_val, 0.0)
        return abs(net) > (threshold_fraction * equity)
    except Exception:
        return False


# ---------------- Price ticks buffer helper ----------------
_price_ticks = deque()


def feed_price_tick(price: float) -> None:
    """
    Append a price tick (timestamp, price) into the rolling deque _price_ticks.
    Keeps data for VOL_WINDOW_SECONDS seconds (used by estimate_short_volatility).
    """
    try:
        ts = time.time()
        _price_ticks.append((ts, float(price)))
        while _price_ticks and _price_ticks[0][0] < ts - VOL_WINDOW_SECONDS:
            _price_ticks.popleft()
    except Exception:
        return


# ---------------- Reduce positions to safe level (implementation) ----------------
async def reduce_positions_to_safe_level(target_fraction: float = 0.1):
    """
    将净暴露降到 equity * target_fraction 以内（示例实现）。
    - target_fraction: 目标净暴露占 equity 的比例，例如 0.1 表示 10%。
    注意：该实现为示例，使用市价/IOC 下单可能导致滑点，请在 testnet 验证并按需改用限价分批。
    """
    try:
        equity = float(account_equity_usdt or initial_equity_usdt or 0.0)
        if equity <= 0:
            log_action("风控", "账户权益未知或为0，无法降仓", "warning")
            return
        # compute current net exposure (USDT)
        net = 0.0
        positions_to_reduce = []
        for k, v in position_info.items():
            # skip balance-only entries
            if str(k).startswith("BAL-"):
                continue
            usdt_val = v.get("usdt_value", None)
            if usdt_val is None:
                pos = safe_float(v.get("pos", 0.0))
                avg_px = safe_float(v.get("avg_px", current_price or 0.0))
                ct = safe_float(v.get("ctVal", CONTRACT_INFO.get("ctVal", 1.0)))
                est = pos * avg_px * (ct or 1.0)
                usdt_val = est
            net += safe_float(usdt_val, 0.0)
            positions_to_reduce.append((k, v))
        target_exposure = equity * target_fraction
        if abs(net) <= target_exposure:
            log_action("风控", "净暴露在目标范围内，无需降仓", "info", {"net": net, "target": target_exposure})
            return
        reduce_amount = abs(net) - target_exposure
        log_action("风控", f"开始降仓，目标减仓金额约 {reduce_amount:.4f} USDT", "warning")
        remaining = reduce_amount
        # Naive reduction: iterate positions and submit opposite market IOC orders until reduce_amount <= 0
        for (k, v) in positions_to_reduce:
            inst = k.split("-")[0] if "-" in k else SYMBOL
            pos_size = safe_float(v.get("pos", 0.0))
            if pos_size == 0:
                continue
            avg_px = safe_float(v.get("avg_px", current_price or 0.0))
            notional = abs(pos_size) * avg_px * v.get("ctVal", CONTRACT_INFO.get("ctVal", 1.0)) if avg_px and pos_size else 0.0
            if pos_size > 0:
                side = "sell"
            else:
                side = "buy"
            proportion = min(1.0, remaining / (notional + 1e-12))
            sz_to_close = abs(pos_size) * proportion
            sz_s = str(round_to_min_size(sz_to_close))
            if float(sz_s) <= 0:
                continue
            try:
                await rate_limiter.wait_for(1, max_per_window=60, window_seconds=2)
                resp = await asyncio.to_thread(trade_api.place_order, instId=inst, tdMode="isolated", side=side, ordType="market", sz=sz_s)
                log_action("风控", f"降仓下单 inst={inst} side={side} sz={sz_s}", "info", resp)
            except Exception as e:
                log_action("风控", f"降仓下单异常: {e}", "error", exc_info=True)
            remaining -= notional * proportion
            if remaining <= 0:
                break
        log_action("风控", "降仓动作完成（示例实现）", "info")
    except Exception as e:
        log_action("风控", f"降仓异常: {e}", "error", exc_info=True)


# ---------------- WebSocket message handlers ----------------
def _handle_account_ws_entry(entry: dict):
    try:
        data = entry.get("data", []) or []
        if not data:
            return
        snapshot = data[0]
        total_eq = snapshot.get("totalEq") or snapshot.get("adjEq") or ""
        if total_eq:
            try:
                global account_equity_usdt, initial_equity_usdt
                account_equity_usdt = float(total_eq)
                if initial_equity_usdt == 0.0:
                    initial_equity_usdt = account_equity_usdt
            except Exception:
                pass
        details = snapshot.get("details", []) or []
        for d in details:
            ccy = d.get("ccy")
            if not ccy:
                continue
            avail = safe_float(d.get("availBal", 0.0))
            eq = safe_float(d.get("eq", 0.0))
            try:
                position_info[f"BAL-{ccy}"]["pos"] = avail
                position_info[f"BAL-{ccy}"]["avg_px"] = 0.0
                position_info[f"BAL-{ccy}"]["usdt_value"] = eq
            except Exception:
                position_info[f"BAL-{ccy}"] = {"pos": avail, "avg_px": 0.0, "usdt_value": eq}
        log_action("WS账户", "处理 account 推送", "debug", {"totalEq": total_eq})
    except Exception as e:
        log_action("WS账户处理", f"异常: {e}", "error", exc_info=True)


def _handle_order_ws_entry(entry: dict):
    try:
        ord_id = entry.get("ordId") or ""
        cl = entry.get("clOrdId") or ""
        trade_id = entry.get("tradeId") or ""
        state = entry.get("state") or ""
        fill_sz = safe_float(entry.get("fillSz", 0))
        acc_fill = safe_float(entry.get("accFillSz", 0))
        req_id = entry.get("reqId") or ""
        if req_id and req_id in seen_reqids:
            return
        if req_id:
            seen_reqids.add(req_id)
        if trade_id:
            if trade_id in seen_trade_ids:
                return
            seen_trade_ids.add(trade_id)
        if not trade_id and state == "filled" and ord_id:
            if ord_id in seen_filled_ordids:
                return
            seen_filled_ordids.add(ord_id)
        key = cl or ord_id or generate_order_id("ws")
        ao = active_orders.get(key, {})
        ao.update({
            "ord_id": ord_id,
            "cl": cl,
            "state": state,
            "fillSz": fill_sz,
            "accFillSz": acc_fill,
            "tradeId": trade_id,
            "raw": entry,
            "last_update": time.time()
        })
        active_orders[key] = ao
        log_action("WS订单", f"更新订单 {key} state={state}", "debug", ao)
        if entry.get("tradeId") or str(state).lower() in ("filled", "partially_filled", "partial-filled"):
            try:
                order_side = (entry.get("side") or "").lower() or "buy"
                our_filled_side = order_side
                cl_local = cl or ao.get("cl") or ""
                async def _update_and_handle():
                    async with orders_lock:
                        ao = active_orders.get(cl_local, {})
                        ao.update({"raw_ws": entry, "state_ws": state, "last_update_ws": time.time()})
                        active_orders[cl_local] = ao
                    try:
                        record_fill_event(our_filled_side, entry)
                        asyncio.create_task(on_fill_event(cl_local, our_filled_side, entry))
                    except Exception:
                        pass
                asyncio.create_task(_update_and_handle())
            except Exception:
                pass
    except Exception as e:
        log_action("WS订单处理", f"异常: {e}", "error", exc_info=True)


def _handle_positions_ws_entry(entry: dict):
    try:
        inst = entry.get("instId") or SYMBOL
        pos = safe_float(entry.get("pos", 0))
        pos_side = (entry.get("posSide") or "net").lower()
        if pos_side == "net":
            side = "long" if pos >= 0 else "short"
            size = abs(pos)
        else:
            side = pos_side
            size = abs(pos)
        key = f"{inst}-{side}"
        # store pos and avg_px
        avg_px = safe_float(entry.get("avgPx", 0))
        position_info[key]["pos"] = pos if pos_side == "net" else size
        position_info[key]["avg_px"] = avg_px
        # compute signed usdt_value: long positive, short negative
        try:
            ct = safe_float(entry.get("ctVal", CONTRACT_INFO.get("ctVal", 1.0)))
        except Exception:
            ct = CONTRACT_INFO.get("ctVal", 1.0) or 1.0
        # signed exposure: pos (can be negative) * avg_px * ct
        signed_usdt = float(pos) * float(avg_px or current_price or 0.0) * float(ct)
        position_info[key]["usdt_value"] = signed_usdt
        position_info[key]["ctVal"] = ct
        log_action("WS仓位", f"{key} -> {size}", "debug", position_info[key])
    except Exception as e:
        log_action("WS仓位处理", f"异常: {e}", "error", exc_info=True)


def _handle_balance_ws_entry(entry: dict):
    log_action("WS余额", "收到 balance_and_position 更新", "debug", entry)


def _handle_fills_ws_entry(entry: dict):
    trade_id = entry.get("tradeId")
    if not trade_id:
        return
    if trade_id in seen_trade_ids:
        return
    seen_trade_ids.add(trade_id)
    ord_id = entry.get("ordId") or ""
    cl = entry.get("clOrdId") or ""
    key = cl or ord_id
    ao = active_orders.get(key, {})
    ao.update({
        "tradeId": trade_id,
        "fillSz": safe_float(entry.get("fillSz", 0)),
        "fillPx": safe_float(entry.get("fillPx", 0)),
        "last_update": time.time()
    })
    active_orders[key] = ao
    try:
        record_fill_event(entry.get("side") or "buy", entry)
        asyncio.create_task(on_fill_event(cl or ao.get("cl",""), entry.get("side") or "buy", entry))
    except Exception:
        pass


def _ws_message_callback(message: Any):
    try:
        data = message
        if isinstance(message, str):
            try:
                data = json.loads(message)
            except Exception:
                log_action("WS", "非 JSON 消息", "debug", {"raw": message})
                return
        if "event" in data and data.get("event"):
            log_action("WS 事件", f"event={data.get('event')}", "debug", data.get("arg"))
        arg = data.get("arg") or {}
        channel = arg.get("channel") or data.get("channel")
        if channel == "orders":
            payloads = data.get("data", []) or []
            if isinstance(payloads, dict):
                payloads = [payloads]
            for p in payloads:
                _handle_order_ws_entry(p)
            return
        if channel == "positions":
            payloads = data.get("data", []) or []
            if isinstance(payloads, dict):
                payloads = [payloads]
            for p in payloads:
                _handle_positions_ws_entry(p)
            return
        if channel == "balance_and_position":
            payloads = data.get("data", []) or []
            for p in payloads:
                _handle_balance_ws_entry(p)
            return
        if channel == "fills":
            payloads = data.get("data", []) or []
            for p in payloads:
                _handle_fills_ws_entry(p)
            return
        if channel == "account":
            _handle_account_ws_entry(data)
            return
        log_action("WS 未知消息", "未处理的频道/消息", "debug", data)
    except Exception as e:
        log_action("WS 回调", f"异常: {e}", "error", exc_info=True)


# ---------------- WS keepalive ----------------
_ws_last_recv = time.time()
_ws_ping_task: Optional[asyncio.Task] = None
_WS_PING_INTERVAL = 20
_WS_PONG_WAIT = 5


def _ws_mark_recv():
    global _ws_last_recv
    _ws_last_recv = time.time()


async def _ws_ping_loop(get_ws_callable, interval=_WS_PING_INTERVAL, pong_wait=_WS_PONG_WAIT):
    """
    Robust ping/pong loop:
    - Try multiple ways to send ping (ws.ping, inner._ws, ws.ws, fallback).
    - If cannot send or no pong received within pong_wait, attempt reconnect with simple backoff.
    - Avoid raising out of loop; handle exceptions and continue.
    """
    backoff_seconds = 1.0
    max_backoff = 30.0
    try:
        while True:
            await asyncio.sleep(interval)
            ws = get_ws_callable()
            if ws is None:
                # no instance, try reconnect with backoff
                log_action("WS 保活", "没有 WS 实例，等待并重试", "debug")
                await asyncio.sleep(backoff_seconds)
                backoff_seconds = min(max_backoff, backoff_seconds * 1.5)
                continue
            # reset backoff when we have an instance
            backoff_seconds = 1.0
            # 近期已有消息则跳过 ping
            if time.time() - _ws_last_recv < interval:
                continue
            try:
                sent = False
                # 1) prefer coroutine ping()
                if hasattr(ws, "ping") and asyncio.iscoroutinefunction(getattr(ws, "ping")):
                    await ws.ping()
                    sent = True
                    log_action("WS 保活", "通过 ws.ping() 发送 ping", "debug")
                elif hasattr(ws, "ping") and callable(getattr(ws, "ping")):
                    await asyncio.to_thread(ws.ping)
                    sent = True
                    log_action("WS 保活", "通过 ws.ping() (sync) 发送 ping", "debug")
                # 2) inner attributes commonly used by wrappers
                elif hasattr(ws, "_ws"):
                    inner = getattr(ws, "_ws")
                    if inner is not None:
                        if hasattr(inner, "ping"):
                            if asyncio.iscoroutinefunction(getattr(inner, "ping")):
                                await inner.ping()
                            else:
                                await asyncio.to_thread(inner.ping)
                            sent = True
                            log_action("WS 保活", "通过 ws._ws.ping() 发送 ping", "debug")
                        elif hasattr(inner, "send"):
                            if asyncio.iscoroutinefunction(getattr(inner, "send")):
                                await inner.send("ping")
                            else:
                                await asyncio.to_thread(inner.send, "ping")
                            sent = True
                            log_action("WS 保活", "通过 ws._ws.send() 发送 ping", "debug")
                elif hasattr(ws, "ws"):
                    inner = getattr(ws, "ws")
                    if inner is not None:
                        if hasattr(inner, "ping"):
                            if asyncio.iscoroutinefunction(getattr(inner, "ping")):
                                await inner.ping()
                            else:
                                await asyncio.to_thread(inner.ping)
                            sent = True
                            log_action("WS 保活", "通过 ws.ws.ping() 发送 ping", "debug")
                        elif hasattr(inner, "send"):
                            if asyncio.iscoroutinefunction(getattr(inner, "send")):
                                await inner.send("ping")
                            else:
                                await asyncio.to_thread(inner.send, "ping")
                            sent = True
                            log_action("WS 保活", "通过 ws.ws.send() 发送 ping", "debug")
                # 3) fallback to ws.send if exists
                elif hasattr(ws, "send"):
                    if asyncio.iscoroutinefunction(getattr(ws, "send")):
                        await ws.send("ping")
                    else:
                        await asyncio.to_thread(ws.send, "ping")
                    sent = True
                    log_action("WS 保活", "通过 ws.send() 发送 ping (fallback)", "debug")

                if not sent:
                    # 无法发送 ping：记录并尝试重建连接（但用 backoff 防止风暴）
                    log_action("WS 保活", "WS 实例不支持发送 ping (no ping/send/_ws/ws)", "warning")
                    try:
                        await stop_private_ws()
                    except Exception:
                        pass
                    await asyncio.sleep(backoff_seconds)
                    asyncio.create_task(start_private_ws())
                    backoff_seconds = min(max_backoff, backoff_seconds * 1.5)
                    continue
            except Exception as e:
                # 发送失败：记录并重连（带 backoff）
                log_action("WS 保活", f"发送 ping 失败: {e}", "warning", exc_info=True)
                try:
                    await stop_private_ws()
                except Exception:
                    pass
                await asyncio.sleep(backoff_seconds)
                asyncio.create_task(start_private_ws())
                backoff_seconds = min(max_backoff, backoff_seconds * 1.5)
                continue

            # 等待 pong_wait，看是否有任何消息/心跳到达
            await asyncio.sleep(pong_wait)
            if time.time() - _ws_last_recv >= pong_wait:
                log_action("WS 保活", "未收到 pong/消息，重连", "warning")
                try:
                    await stop_private_ws()
                except Exception:
                    pass
                await asyncio.sleep(backoff_seconds)
                asyncio.create_task(start_private_ws())
                backoff_seconds = min(max_backoff, backoff_seconds * 1.5)
    except asyncio.CancelledError:
        return
    except Exception as e:
        log_action("WS 保活", f"异常: {e}", "error", exc_info=True)


# ---------------- Public / Private WS start/stop ----------------
async def start_private_ws():
    global _ws_instance, _ws_ping_task
    if PrivateWs is None:
        log_action("WS", "PrivateWs SDK 未安装，无法启动私有 WS", "error")
        return None
    try:
        if str(OKX_FLAG) == "1":
            ws_url = "wss://wspap.okx.com:8443/ws/v5/private"
        else:
            ws_url = "wss://ws.okx.com:8443/ws/v5/private"
        log_action("WS", f"Connecting private WS to {ws_url}", "info")
        ws = PrivateWs(apiKey=API_KEY, passphrase=PASSPHRASE, secretKey=SECRET_KEY, url=ws_url, useServerTime=False)
        await ws.start()
        _ws_instance = ws
        log_action("WS", "私有 WS 已启动", "info")
        args = [
            {"channel": "positions", "instType": "ANY"},
            {"channel": "balance_and_position"},
            {"channel": "orders", "instType": "ANY"},
            {"channel": "account"}
        ]
        if ENABLE_FILLS_CHANNEL:
            args.append({"channel": "fills"})
        await ws.subscribe(args, callback=_ws_message_callback)
        log_action("WS", "已订阅私有频道", "info", {"args": args})
        if _ws_ping_task is None or _ws_ping_task.done():
            _ws_ping_task = asyncio.create_task(_ws_ping_loop(lambda: _ws_instance))
        return ws
    except Exception as e:
        log_action("WS 启动", f"失败: {e}", "error", exc_info=True)
        return None


async def stop_private_ws():
    global _ws_instance, _ws_ping_task
    try:
        if _ws_instance:
            try:
                await _ws_instance.stop()
            except Exception:
                pass
            _ws_instance = None
        if _ws_ping_task:
            _ws_ping_task.cancel()
            _ws_ping_task = None
        log_action("WS", "私有 WS 已停止", "info")
    except Exception as e:
        log_action("WS 停止", f"异常: {e}", "warning", exc_info=True)


async def start_public_ws():
    global _public_ws_instance
    if PublicWs is None:
        log_action("Public WS", "PublicWs SDK 未安装，跳过", "warning")
        return None
    try:
        if str(OKX_FLAG) == "1":
            public_url = "wss://wspap.okx.com:8443/ws/v5/public"
        else:
            public_url = "wss://ws.okx.com:8443/ws/v5/public"
        ws = PublicWs(url=public_url)
        await ws.start()
        _public_ws_instance = ws
        args = [{"channel": "tickers", "instId": SYMBOL}]
        await ws.subscribe(args, callback=_public_ws_ticker_callback)
        log_action("Public WS", "已订阅 tickers", "info", {"inst": SYMBOL, "url": public_url})
        return ws
    except Exception as e:
        log_action("Public WS", f"启动失败: {e}", "error", exc_info=True)
        return None


async def stop_public_ws():
    global _public_ws_instance
    try:
        if _public_ws_instance:
            try:
                await _public_ws_instance.stop()
            except Exception:
                pass
            _public_ws_instance = None
        log_action("Public WS", "已停止", "info")
    except Exception as e:
        log_action("Public WS 停止", f"异常: {e}", "warning", exc_info=True)


def _public_ws_ticker_callback(message: Any):
    global current_price, last_price, price_source, best_bid, best_ask
    try:
        data = message
        if isinstance(message, str):
            try:
                data = json.loads(message)
            except Exception:
                return
        if "event" in data:
            return
        arg = data.get("arg") or {}
        channel = arg.get("channel") or data.get("channel")
        if channel != "tickers":
            return
        payloads = data.get("data", []) or []
        if isinstance(payloads, dict):
            payloads = [payloads]
        for p in payloads:
            price = None
            for k in ("last", "lastPx", "price"):
                if k in p:
                    price = safe_float(p.get(k))
                    break
            if price is None:
                bid = safe_float(p.get("bidPx", 0))
                ask = safe_float(p.get("askPx", 0))
                if bid and ask:
                    price = (bid + ask) / 2.0
                elif bid:
                    price = bid
                elif ask:
                    price = ask
            if price is None:
                continue
            best_bid = safe_float(p.get("bidPx", best_bid))
            best_ask = safe_float(p.get("askPx", best_ask))
            last_price = current_price
            current_price = float(price)
            price_source = "ws_ticker"
            try:
                feed_price_tick(current_price)
            except Exception:
                pass
    except Exception:
        pass


# ---------------- Strategy helpers (continuous-eaten, gatekeeper, dynamic offset) ----------------
N_CONSEC = 3
WINDOW_SECONDS = 60
MIN_FILLS_WINDOW = 5
P_THRESHOLD = 0.7
PAUSE_SECONDS_AFTER_CONSEC = 120
SCALE_DOWN_FACTOR = 0.3

SAFETY_MARGIN_USDT = 0.5
MAX_REQUIRED_MOVE_PCT = 0.015

MIN_OFFSET_PCT = 0.0008
VOL_K = 1.0
VOL_WINDOW_SECONDS = 60

_recent_fills = deque()
_consec_same_side = 0
_last_fill_side: Optional[str] = None
_paused_until = 0.0
_trend_watch_until = 0.0
_mark_scale_down_next = False

_price_ticks = deque()

def record_fill_event(side: str, fill_info: Dict[str, Any]) -> None:
    global _consec_same_side, _last_fill_side, _recent_fills
    ts = time.time()
    if _last_fill_side == side:
        _consec_same_side += 1
    else:
        _consec_same_side = 1
        _last_fill_side = side
    _recent_fills.append((ts, side, fill_info))
    while _recent_fills and _recent_fills[0][0] < ts - WINDOW_SECONDS:
        _recent_fills.popleft()

def check_window_rule() -> bool:
    if len(_recent_fills) < MIN_FILLS_WINDOW:
        return False
    same = sum(1 for (_, s, _) in _recent_fills if s == _last_fill_side)
    frac = same / len(_recent_fills)
    return frac >= P_THRESHOLD

async def on_fill_event(cl: str, side: str, fill_info: Dict[str, Any]):
    global _paused_until, _trend_watch_until, _mark_scale_down_next, _consec_same_side
    record_fill_event(side, fill_info)
    window_trigger = check_window_rule()
    if _consec_same_side >= N_CONSEC or window_trigger:
        _paused_until = time.time() + PAUSE_SECONDS_AFTER_CONSEC
        _trend_watch_until = max(_trend_watch_until, time.time() + PAUSE_SECONDS_AFTER_CONSEC)
        _mark_scale_down_next = True
        try:
            other_cl = get_other_cl_of_active_pair(cl)
            if other_cl:
                await cancel_order_by_cl(other_cl)
        except Exception:
            pass
        try:
            log_action("风控", f"连续被吃保护触发 side={side} consec={_consec_same_side}", "warning", {"fill": fill_info})
        except Exception:
            pass
        try:
            if net_exposure_exceeds_threshold():
                asyncio.create_task(reduce_positions_to_safe_level())
        except Exception:
            pass
        return
    return

def is_paused() -> bool:
    return time.time() < _paused_until

def mark_and_consume_scale_down() -> bool:
    global _mark_scale_down_next
    if _mark_scale_down_next:
        _mark_scale_down_next = False
        return True
    return False

def should_place_pair(position_value: float,
                      fee_maker: float,
                      fee_taker: float,
                      funding_rate_per_8h: float,
                      expected_hold_seconds: float,
                      expected_slippage_pct: float,
                      safety_margin_usdt: float = SAFETY_MARGIN_USDT,
                      max_required_move_pct: float = MAX_REQUIRED_MOVE_PCT) -> Dict[str, Any]:
    roundtrip_fee_usdt = position_value * (fee_maker + fee_maker)
    funding_usdt = position_value * funding_rate_per_8h * (expected_hold_seconds / (8*3600))
    slippage_usdt = position_value * expected_slippage_pct
    total_cost_usdt = roundtrip_fee_usdt + funding_usdt + slippage_usdt + safety_margin_usdt
    required_move_pct = total_cost_usdt / position_value
    can_place = (required_move_pct < max_required_move_pct)
    return {
        "roundtrip_fee_usdt": roundtrip_fee_usdt,
        "funding_usdt": funding_usdt,
        "slippage_usdt": slippage_usdt,
        "total_cost_usdt": total_cost_usdt,
        "required_move_pct": required_move_pct,
        "can_place": can_place
    }

# ---------------- Main loops ----------------
async def main_loop_once():
    ok = await fetch_instrument_info()
    if not ok:
        log_action("主流程", "未能加载合约信息，退出", "error")
        return
    await update_price_from_rest()
    await fetch_account_and_positions()
    log_action("主流程", "一次循环完成", "info")


async def main_loop_continuous():
    private_task = asyncio.create_task(start_private_ws())
    public_task = None
    if ENABLE_PUBLIC_TICKER:
        public_task = asyncio.create_task(start_public_ws())
    try:
        while True:
            try:
                await main_loop_once()
            except Exception as e:
                log_action("主循环", f"异常: {e}", "error", exc_info=True)
            await asyncio.sleep(5)
    finally:
        try:
            await stop_private_ws()
        except Exception:
            pass
        if public_task:
            try:
                await stop_public_ws()
            except Exception:
                pass


# ---------------- Entrypoint ----------------
if __name__ == "__main__":
    initialize_clients()
    log_action("启动", f"OKX_FLAG={OKX_FLAG} (测试网=1)", "info")
    asyncio.run(main_loop_continuous())
