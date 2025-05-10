import numpy as np


def backtest_strategy(
        df,
        initial_balance=10000,
        buy_ratio=0.5,  # 买入资金比例（0 < ratio ≤ 1）
        sell_ratio=0.5,  # 卖出持仓比例（0 < ratio ≤ 1）
        buy_fee_rate=0.001,
        sell_fee_rate=0.001
):
    """支持比例交易的回测策略"""
    balance = initial_balance  # 可用资金
    holdings = 0.0  # 持仓数量
    history = []

    for idx, row in df.iterrows():
        signal, close_price = row['signal'], row['c']

        if signal == 1 and balance > 0:
            # 按比例买入：使用buy_ratio比例的可用资金
            planned_invest = balance * buy_ratio
            available_invest = planned_invest * (1 - buy_fee_rate)  # 扣除手续费后的实际使用金额
            amount = available_invest / close_price  # 实际购买数量

            history.append({
                'time': row['ts'],
                'type': 'buy',
                'price': close_price,
                'ratio': buy_ratio,  # 记录使用的买入比例
                'planned_invest': planned_invest,
                'actual_invest': available_invest,  # 扣除手续费后的金额
                'amount': amount,
                'balance_after': balance - planned_invest,  # 剩余可用资金（包含手续费部分）
                'holdings_after': holdings + amount
            })

            holdings += amount
            balance -= planned_invest  # 扣除计划投入的资金（含手续费）

        elif signal == -1 and holdings > 0:
            # 按比例卖出：卖出sell_ratio比例的持仓
            planned_sell = holdings * sell_ratio  # 计划卖出数量
            total_proceeds = planned_sell * close_price
            available_proceeds = total_proceeds * (1 - sell_fee_rate)  # 扣除手续费后的到账金额

            history.append({
                'time': row['ts'],
                'type': 'sell',
                'price': close_price,
                'ratio': sell_ratio,  # 记录使用的卖出比例
                'planned_sell': planned_sell,
                'actual_proceeds': available_proceeds,  # 扣除手续费后的到账金额
                'amount': planned_sell,
                'balance_after': balance + available_proceeds,  # 可用资金增加
                'holdings_after': holdings - planned_sell
            })

            balance += available_proceeds
            holdings -= planned_sell  # 减少已卖出的持仓

    # 回测结束时处理剩余持仓（可选：是否按最后价格清仓）
    if holdings > 0:
        final_price = df['c'].iloc[-1]
        total_proceeds = holdings * final_price
        available_proceeds = total_proceeds * (1 - sell_fee_rate)
        balance += available_proceeds
        holdings = 0

    return {
        'initial_balance': initial_balance,
        'final_balance': balance,
        'final_holdings': holdings,
        'return': (balance - initial_balance) / initial_balance if initial_balance != 0 else 0,
        'trade_history': history,
        'buy_ratio': buy_ratio,
        'sell_ratio': sell_ratio,
        'buy_fee_rate': buy_fee_rate,
        'sell_fee_rate': sell_fee_rate
    }


def evaluate_performance(backtest_result):
    """评估含比例交易的策略绩效"""
    history = backtest_result['trade_history']
    returns = []

    # 匹配买卖交易（按顺序配对）
    buy_trades = [t for t in history if t['type'] == 'buy']
    sell_trades = [t for t in history if t['type'] == 'sell']

    for buy, sell in zip(buy_trades, sell_trades):
        buy_price = buy['price']
        sell_price = sell['price']
        if buy_price != 0:
            returns.append((sell_price - buy_price) / buy_price)

    win_rate = sum(r > 0 for r in returns) / len(returns) if returns else 0
    return {
        'total_return': backtest_result['return'],
        'win_rate': win_rate,
        'max_drawdown': calculate_max_drawdown(history),
        'avg_return': np.mean(returns) if returns else 0,
        'num_trades': len(returns),
        'buy_ratio': backtest_result['buy_ratio'],
        'sell_ratio': backtest_result['sell_ratio']
    }


def calculate_max_drawdown(history):
    """适配比例交易的最大回撤计算"""
    if not history:
        return 0.0

    # 构建资金曲线（资金 + 持仓市值）
    equity = [history[0]['balance_after'] if history[0]['type'] == 'buy' else history[0]['balance']]

    for trade in history:
        if trade['type'] == 'buy':
            # 买入后：剩余资金 + 持仓市值
            current_value = trade['balance_after'] + trade['holdings_after'] * trade['price']
        elif trade['type'] == 'sell':
            # 卖出后：可用资金 + 剩余持仓市值（若有）
            current_value = trade['balance_after'] + trade['holdings_after'] * trade['price']
        else:
            current_value = equity[-1]  # 无操作时价值不变
        equity.append(current_value)

    peak, max_drawdown = equity[0], 0.0
    for e in equity:
        if e > peak:
            peak = e
        if peak != 0:
            drawdown = (peak - e) / peak
            max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown


def calculate_ma_signals(df, short_window=5, long_window=20):
    """计算双均线信号（保留原始逻辑）"""
    df['ma_short'] = df['c'].rolling(short_window).mean()
    df['ma_long'] = df['c'].rolling(long_window).mean()
    df['signal'] = np.where(df['ma_short'] > df['ma_long'], 1, np.where(df['ma_short'] < df['ma_long'], -1, 0))
    return df.dropna(subset=['ma_short', 'ma_long']).reset_index(drop=True)