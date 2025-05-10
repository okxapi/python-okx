from dataclasses import dataclass
from datetime import datetime

@dataclass
class KlineData:
    ts: datetime          # 开始时间
    o: float              # 开盘价
    h: float              # 最高价
    l: float              # 最低价
    c: float              # 收盘价
    vol: float            # 交易货币数量（如BTC）
    vol_ccy: float        # 计价货币数量（如USDT）
    vol_ccy_quote: float  # 计价货币单位交易量
    confirm: int          # K线状态（0=未完结，1=已完结）