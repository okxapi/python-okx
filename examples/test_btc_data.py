"""
测试脚本：验证 BTC-USDT 数据获取功能（实盘数据）
"""

from get_btc_market_data import (
    get_btc_ticker,
    get_kline_data,
    get_historical_kline_data,
    analyze_ma20
)


def test_all_functions():
    """测试所有数据获取函数"""
    print("测试开始...\n")

    # 测试 1: 获取市价（实盘）
    print("[测试 1] 获取市价（实盘）...")
    ticker = get_btc_ticker('BTC-USDT', use_live_trading=True)
    assert ticker is not None, "市价获取失败"
    assert ticker['last_price'] is not None, "最新价格应为非空"
    print(f"  [OK] 市价获取成功：${ticker['last_price']}")

    # 测试 2: 获取 15 分钟 K 线（实盘）
    print("\n[测试 2] 获取 15 分钟 K 线（实盘）...")
    kline_15m = get_kline_data('BTC-USDT', bar='15m', limit=50, use_live_trading=True)
    assert kline_15m is not None, "15 分钟 K 线获取失败"
    assert not kline_15m.empty, "15 分钟 K 线数据为空"
    assert len(kline_15m) > 0, "K 线数据应包含至少一条记录"
    assert 'close' in kline_15m.columns, "K 线数据应包含收盘价列"
    print(f"  [OK] 15 分钟 K 线获取成功：{len(kline_15m)} 条数据")

    # 测试 3: 获取 1 小时 K 线（实盘）
    print("\n[测试 3] 获取 1 小时 K 线（实盘）...")
    kline_1h = get_kline_data('BTC-USDT', bar='1H', limit=50, use_live_trading=True)
    assert kline_1h is not None, "1 小时 K 线获取失败"
    assert not kline_1h.empty, "1 小时 K 线数据为空"
    print(f"  [OK] 1 小时 K 线获取成功：{len(kline_1h)} 条数据")

    # 测试 4: 计算 15 分钟 MA20
    print("\n[测试 4] 计算 15 分钟 MA20...")
    analysis_15m = analyze_ma20(kline_15m, '15m')
    assert analysis_15m is not None, "MA20 分析失败"
    assert analysis_15m['current_price'] is not None, "当前价格应为非空"
    assert analysis_15m['ma20'] is not None, "MA20 应为非空"
    print(f"  [OK] 15 分钟 MA20 计算成功：MA20=${analysis_15m['ma20']:.2f}")

    # 测试 5: 计算 1 小时 MA20
    print("\n[测试 5] 计算 1 小时 MA20...")
    analysis_1h = analyze_ma20(kline_1h, '1H')
    assert analysis_1h is not None, "MA20 分析失败"
    assert analysis_1h['ma20'] is not None, "MA20 应为非空"
    print(f"  [OK] 1 小时 MA20 计算成功：MA20=${analysis_1h['ma20']:.2f}")

    # 测试 6: 获取历史 K 线（实盘）
    print("\n[测试 6] 获取历史 K 线（实盘）...")
    hist_kline = get_historical_kline_data('BTC-USDT', bar='1H', limit=50, use_live_trading=True)
    assert hist_kline is not None, "历史 K 线获取失败"
    print(f"  [OK] 历史 K 线获取成功：{len(hist_kline)} 条数据")

    print("\n" + "=" * 50)
    print("所有测试通过！")
    print("=" * 50)

    return True


if __name__ == '__main__':
    test_all_functions()
