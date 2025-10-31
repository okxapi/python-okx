#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETH perpetual trading bot for OKX (SDK-only, testnet-ready).
- This file is a consolidated version including:
  * SDK-only initialization (Account/Trade/MarketData, PrivateWs/PublicWs)
  * REST helpers (fetch instrument, balance, positions, place orders)
  * WS handling (orders/positions/balance/tickers), ping/pong keepalive
  * Strategy: single-layer moving grid (pair) with:
      - continuous-eaten protection
      - gatekeeper (cost check)
      - dynamic offset (vol-based)
      - place_pair_if_ok helper (with pair_id bookkeeping and compensation)
- NOTE: Replace the API_KEY/SECRET/PASSPHRASE with your testnet keys,
  or set environment variables as preferred.
"""

import asyncio
import time
import json
import logging
import random
import string
import os
from datetime import datetime, timezone
from collections import defaultdict, deque
from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Optional, Dict, Any, List
import math
import sys

# ---------------- Configuration: put testnet credentials here (for testing only) ----------------
API_KEY = os.getenv("OKX_API_KEY", "YOUR_TESTNET_API_KEY")
SECRET_KEY = os.getenv("OKX_SECRET_KEY", "YOUR_TESTNET_SECRET")
PASSPHRASE = os.getenv("OKX_PASSPHRASE", "YOUR_TESTNET_PASSPHRASE")
OKX_FLAG = os.getenv("OKX_FLAG", "1")  # "1" testnet, "0" mainnet

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

# Remove existing handlers to avoid duplication
for h in list(logger.handlers):
    logger.removeHandler(h)

# File handler (UTF-8)
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(fh)

# Ensure stdout uses UTF-8 if possible
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
    # timezone-aware UTC timestamp
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
        # 最后兜底：替换不可编码字符再写入（避免程序崩溃）
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

# Strategy/config example
STRATEGY = {
    "base_notional_fraction": 0.25,  # fraction of equity*leverage per pair
    "leverage": 5,
    "price_offset": 0.001,  # default; dynamic offset will override
    "expected_hold_seconds": 300,
    "expected_slippage_pct": 0.0002,
    "order_type": "limit",
    "scale_in_enabled": False,
    "scale_step": 0.0,
    "cooldown_after_fill": 0.5
}

# Runtime state
account_equity_usdt = 0.0
initial_equity_usdt = 0.0
current_price = 0.0
last_price = 0.0
price_source = "unknown"

active_orders: Dict[str, dict] = {}
position_info = defaultdict(lambda: {"pos": 0.0, "avg_px": 0.0, "usdt_value": 0.0})

# ---------------- PAIRS & CONCURRENCY LOCK ----------------
active_pairs: Dict[str, dict] = {}          # pair_id -> {buy: {...}, sell: {...}, status, created_at}
orders_lock = asyncio.Lock()                # 用于保护 active_orders/active_pairs 的并发访问

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
                # small spacing
                if now - self.last_request_time < 0.05:
                    await asyncio.sleep(max(0.0, 0.05 - (now - self.last_request_time)))
                self.count += n
                self.last_request_time = time.time()
                return
            await asyncio.sleep(0.05)


rate_limiter = RateLimiter()

# ---------------- Initialization (SDK-only) ----------------
def initialize_clients():
    global account_api, trade_api, market_api
    if Account is None or Trade is None or MarketData is None:
        log_action("初始化", "OKX SDK 未安装，请 pip install okx 或使用官方 SDK", "error")
        raise RuntimeError("OKX SDK not installed")
    account_api = Account.AccountAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
    trade_api = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
    market_api = MarketData.MarketAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, OKX_FLAG)
    log_action("初始化", f"OKX SDK 已初始化 (flag={OKX_FLAG})", "info")


# ---------------- REST helpers (simplified) ----------------
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
    target = SYMBOL
    found = None
    for it in data:
        if it.get("instId") == target:
            found = it
            break
    if not found:
        for it in data:
            if it.get("instId", "").startswith(target.split("-")[0]) and "USDT" in it.get("instId", ""):
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

... (file truncated in this message for brevity) ...