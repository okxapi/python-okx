# BTC-USDT 实盘数据获取程序

获取 BTC-USDT 实盘市价、历史 K 线数据，并计算 MA20 移动平均线。

## 功能

1. **获取市价** - BTC-USDT 当前价格、买卖盘、24 小时统计
2. **15 分钟 K 线** - 获取最新 100 条 15 分钟 K 线并计算 MA20
3. **1 小时 K 线** - 获取最新 100 条 1 小时 K 线并计算 MA20

## 安装依赖

```bash
pip install pandas
pip install -e .  # 安装 okx 包
```

## 使用方法

### 运行主程序

```bash
python examples/get_btc_market_data.py
```

### 运行测试

```bash
python examples/test_btc_data.py
```

### 在代码中使用

```python
from examples.get_btc_market_data import (
    get_btc_ticker,
    get_kline_data,
    analyze_ma20
)

# 获取市价
ticker = get_btc_ticker('BTC-USDT', use_live_trading=True)
print(f"当前价格：${ticker['last_price']}")

# 获取 15 分钟 K 线
kline_15m = get_kline_data('BTC-USDT', bar='15m', limit=100, use_live_trading=True)

# 计算 MA20
analysis = analyze_ma20(kline_15m, '15m')
print(f"MA20: ${analysis['ma20']:.2f}")
print(f"价格 vs MA20: {analysis['price_vs_ma220_pct']:.2f}%")
```

## API 说明

### `get_btc_ticker(inst_id, use_live_trading)`
获取当前市价

| 参数 | 类型 | 说明 |
|------|------|------|
| inst_id | str | 交易对，默认 'BTC-USDT' |
| use_live_trading | bool | 是否使用实盘数据，默认 True |

返回字典包含：`inst_id`, `last_price`, `bid_price`, `ask_price`, `high_24h`, `low_24h`, `volume_24h`, `change_24h`

### `get_kline_data(inst_id, bar, limit, use_live_trading)`
获取 K 线数据

| 参数 | 类型 | 说明 |
|------|------|------|
| inst_id | str | 交易对 |
| bar | str | K 线时间粒度：'15m', '1H', '4H', '1D' 等 |
| limit | int | 获取数量，最大 300 |
| use_live_trading | bool | 是否使用实盘数据 |

返回 pandas DataFrame，包含列：`timestamp`, `open`, `high`, `low`, `close`, `volume`, `datetime`

### `analyze_ma20(df, timeframe)`
分析 MA20 数据

| 参数 | 类型 | 说明 |
|------|------|------|
| df | DataFrame | K 线数据 |
| timeframe | str | 时间周期标识 |

返回字典包含：`current_price`, `ma20`, `price_vs_ma20`, `price_vs_ma20_pct`, `ma20_trend`, `latest_time`

## 输出示例

```
============================================================
BTC-USDT 市场行情分析
============================================================

[1] 当前市价
----------------------------------------
交易对：BTC-USDT
最新价格：$68898.5
买一价：$68865.6
卖一价：$68865.7
24h 最高：$69477.4
24h 最低：$65616.3
24h 成交量：11047.39 BTC

[2] 15 分钟级别 MA20
----------------------------------------
数据点数：100
当前价格：$68898.50
MA20: $68664.74
价格 vs MA20: $233.76 (0.34%)
MA20 趋势：up
最新时间：2026-03-09 16:15:00

[3] 1 小时级别 MA20
----------------------------------------
数据点数：100
当前价格：$68898.50
MA20: $67528.99
价格 vs MA20: $1369.51 (2.03%)
MA20 趋势：up
最新时间：2026-03-09 16:00:00
```

## 注意事项

1. **实盘/模拟盘切换**：设置 `use_live_trading=False` 使用模拟盘数据
2. **数据更新频率**：OKX 市场数据实时推送，建议合理控制请求频率
3. **MA20 计算**：需要至少 20 条数据才能计算出有效的 MA20 值
