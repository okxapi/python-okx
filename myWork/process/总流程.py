# 1. 数据解析
from myWork.process.read import parse_kline_data
from myWork.process.回测 import calculate_ma_signals, backtest_strategy, evaluate_performance

kline_df = parse_kline_data('../sorted_history.csv')

# 2. 计算信号（双均线）
signal_df = calculate_ma_signals(kline_df, short_window=50, long_window=200)

# 3. 执行回测（设置买入50%资金，卖出30%持仓）
backtest_result = backtest_strategy(
    signal_df,
    initial_balance=100000,
    buy_ratio=0.5,       # 每次用50%资金买入
    sell_ratio=0.3,      # 每次卖出30%持仓
    buy_fee_rate=0.001,
    sell_fee_rate=0.001
)

# 4. 评估绩效
performance = evaluate_performance(backtest_result)

# 5. 输出结果
print(f"策略参数：买入比例{performance['buy_ratio']*100}%，卖出比例{performance['sell_ratio']*100}%")
print(f"最终资产：{backtest_result['final_balance'] + backtest_result['final_holdings'] * kline_df['c'].iloc[-1]:.2f} USDT")
print(f"总收益率：{performance['total_return']*100:.2f}%")
print(f"胜率：{performance['win_rate']*100:.2f}%，最大回撤：{performance['max_drawdown']*100:.2f}%")
