"""
获取 BTC-USDT 市价、历史 K 线数据，并计算 MA20

功能：
1. 获取 BTC-USDT 当前市价（ticker）
2. 获取 15 分钟级别历史 K 线并计算 MA20
3. 获取 1 小时级别历史 K 线并计算 MA20
"""

from okx.MarketData import MarketAPI
from okx.PublicData import PublicAPI
from typing import List, Dict, Optional
import pandas as pd


def calculate_ma20(df: pd.DataFrame, price_column: str = 'close') -> pd.Series:
    """计算 20 周期简单移动平均线"""
    return df[price_column].rolling(window=20).mean()


def parse_candlestick_data(candlesticks: List[List[str]]) -> pd.DataFrame:
    """
    解析 K 线数据为 DataFrame

    OKX K 线数据格式（9 列）：
    [时间戳，开盘价，最高价，最低价，收盘价，交易量，交易量*价格，uTx 数量，合约数量]
    OKX 返回的 K 线数据按时间倒序排列（最新的在前）
    """
    if not candlesticks:
        return pd.DataFrame()

    df = pd.DataFrame(candlesticks, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'volume_quote', 'tx_count', 'contracts'
    ])

    # 转换数据类型
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    # 转换时间戳（OKX 返回毫秒级时间戳字符串）
    df['datetime'] = pd.to_datetime(df['timestamp'].astype(float), unit='ms')

    # 按时间正序排列（最早的在前，最新的在后）
    df = df.sort_values('datetime').reset_index(drop=True)

    return df


def get_btc_ticker(inst_id: str = 'BTC-USDT', use_live_trading: bool = True) -> Optional[Dict]:
    """获取 BTC-USDT 当前市价

    Args:
        inst_id: 交易对
        use_live_trading: 是否使用实盘数据（True=实盘，False=模拟盘）
    """
    market_api = MarketAPI(flag='0' if use_live_trading else '1')
    result = market_api.get_ticker(instId=inst_id)

    if result.get('code') == '0' and result.get('data'):
        ticker = result['data'][0]
        return {
            'inst_id': ticker.get('instId'),
            'last_price': ticker.get('last'),
            'bid_price': ticker.get('bidPx'),
            'ask_price': ticker.get('askPx'),
            'high_24h': ticker.get('high24h'),
            'low_24h': ticker.get('low24h'),
            'volume_24h': ticker.get('vol24h'),
            'change_24h': ticker.get('chgUtc24h'),
            'timestamp': ticker.get('ts')
        }
    return None


def get_kline_data(inst_id: str = 'BTC-USDT', bar: str = '15m', limit: int = 100, use_live_trading: bool = True) -> Optional[pd.DataFrame]:
    """
    获取 K 线数据

    Args:
        inst_id: 交易对，如 BTC-USDT
        bar: K 线时间粒度，如 15m, 1H, 4H, 1D 等
        limit: 获取的 K 线数量，最大 300
        use_live_trading: 是否使用实盘数据（True=实盘，False=模拟盘）

    Returns:
        包含 K 线数据的 DataFrame
    """
    market_api = MarketAPI(flag='0' if use_live_trading else '1')
    result = market_api.get_candlesticks(instId=inst_id, bar=bar, limit=str(limit))

    if result.get('code') == '0' and result.get('data'):
        return parse_candlestick_data(result['data'])
    return None


def get_historical_kline_data(inst_id: str = 'BTC-USDT', bar: str = '15m', limit: int = 300, use_live_trading: bool = True) -> Optional[pd.DataFrame]:
    """
    获取历史 K 线数据（top currencies only）

    Args:
        inst_id: 交易对，如 BTC-USDT
        bar: K 线时间粒度
        limit: 获取的 K 线数量，最大 300
        use_live_trading: 是否使用实盘数据（True=实盘，False=模拟盘）

    Returns:
        包含 K 线数据的 DataFrame
    """
    market_api = MarketAPI(flag='0' if use_live_trading else '1')
    result = market_api.get_history_candlesticks(instId=inst_id, bar=bar, limit=str(limit))

    if result.get('code') == '0' and result.get('data'):
        return parse_candlestick_data(result['data'])
    return None


def analyze_ma20(df: pd.DataFrame, timeframe: str) -> Dict:
    """
    分析 MA20 数据

    Returns:
        包含 MA20 分析结果的字典
    """
    if df.empty:
        return {}

    df = df.copy()
    df['ma20'] = calculate_ma20(df, 'close')

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) >= 2 else latest

    result = {
        'timeframe': timeframe,
        'current_price': float(latest['close']),
        'ma20': float(latest['ma20']) if pd.notna(latest['ma20']) else None,
        'ma20_previous': float(previous['ma20']) if pd.notna(previous['ma20']) else None,
        'price_vs_ma20': float(latest['close'] - latest['ma20']) if pd.notna(latest['ma20']) else None,
        'price_vs_ma20_pct': float((latest['close'] / latest['ma20'] - 1) * 100) if pd.notna(latest['ma20']) else None,
        'ma20_trend': 'up' if (pd.notna(latest['ma20']) and pd.notna(previous['ma20']) and latest['ma20'] > previous['ma20']) else 'down',
        'data_points': len(df),
        'latest_time': str(latest['datetime'])
    }

    return result


def main():
    """主函数"""
    print("=" * 60)
    print("BTC-USDT 市场行情分析")
    print("=" * 60)

    # 1. 获取当前市价
    print("\n[1] 当前市价")
    print("-" * 40)
    ticker = get_btc_ticker('BTC-USDT')
    if ticker:
        print(f"交易对：{ticker['inst_id']}")
        print(f"最新价格：${ticker['last_price']}")
        print(f"买一价：${ticker['bid_price']}")
        print(f"卖一价：${ticker['ask_price']}")
        print(f"24h 最高：${ticker['high_24h']}")
        print(f"24h 最低：${ticker['low_24h']}")
        print(f"24h 涨跌：${ticker['change_24h']}")
        print(f"24h 成交量：{ticker['volume_24h']} BTC")
    else:
        print("获取市价失败")

    # 2. 获取 15 分钟 K 线并计算 MA20
    print("\n[2] 15 分钟级别 MA20")
    print("-" * 40)
    kline_15m = get_kline_data('BTC-USDT', bar='15m', limit=100)
    if kline_15m is not None and not kline_15m.empty:
        analysis_15m = analyze_ma20(kline_15m, '15m')
        print(f"数据点数：{analysis_15m['data_points']}")
        print(f"当前价格：${analysis_15m['current_price']:.2f}")
        print(f"MA20: ${analysis_15m['ma20']:.2f}" if analysis_15m['ma20'] else "MA20: 计算中")
        print(f"价格 vs MA20: ${analysis_15m['price_vs_ma20']:.2f} ({analysis_15m['price_vs_ma20_pct']:.2f}%)" if analysis_15m['price_vs_ma20'] else "价格 vs MA20: N/A")
        print(f"MA20 趋势：{analysis_15m['ma20_trend']}")
        print(f"最新时间：{analysis_15m['latest_time']}")
    else:
        print("获取 15 分钟 K 线失败")

    # 3. 获取 1 小时 K 线并计算 MA20
    print("\n[3] 1 小时级别 MA20")
    print("-" * 40)
    kline_1h = get_kline_data('BTC-USDT', bar='1H', limit=100)
    if kline_1h is not None and not kline_1h.empty:
        analysis_1h = analyze_ma20(kline_1h, '1H')
        print(f"数据点数：{analysis_1h['data_points']}")
        print(f"当前价格：${analysis_1h['current_price']:.2f}")
        print(f"MA20: ${analysis_1h['ma20']:.2f}" if analysis_1h['ma20'] else "MA20: 计算中")
        print(f"价格 vs MA20: ${analysis_1h['price_vs_ma20']:.2f} ({analysis_1h['price_vs_ma20_pct']:.2f}%)" if analysis_1h['price_vs_ma20'] else "价格 vs MA20: N/A")
        print(f"MA20 趋势：{analysis_1h['ma20_trend']}")
        print(f"最新时间：{analysis_1h['latest_time']}")
    else:
        print("获取 1 小时 K 线失败")

    print("\n" + "=" * 60)

    # 返回所有数据供程序化使用
    return {
        'ticker': ticker,
        'kline_15m': kline_15m,
        'kline_1h': kline_1h,
        'analysis_15m': analyze_ma20(kline_15m, '15m') if kline_15m is not None else None,
        'analysis_1h': analyze_ma20(kline_1h, '1H') if kline_1h is not None else None
    }


if __name__ == '__main__':
    result = main()
