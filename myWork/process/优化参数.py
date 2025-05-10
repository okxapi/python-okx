import itertools
import pandas as pd
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import os

from myWork.process.回测 import calculate_ma_signals, backtest_strategy, evaluate_performance


def process_single_param_combination(kline_df, params, initial_balance, fees, verbose):
    """处理单个参数组合的回测"""
    buy_fee_rate, sell_fee_rate = fees
    short, long_, buy_ratio, sell_ratio = params

    try:
        # 1. 计算信号
        signal_df = calculate_ma_signals(kline_df, short, long_)
        if signal_df.empty:
            if verbose:
                print(f"进程 {os.getpid()}: 警告: 参数组合 {params} 生成的信号为空，跳过")
            return None

        # 2. 执行回测
        backtest_result = backtest_strategy(
            signal_df,
            initial_balance=initial_balance,
            buy_ratio=buy_ratio,
            sell_ratio=sell_ratio,
            buy_fee_rate=buy_fee_rate,
            sell_fee_rate=sell_fee_rate
        )

        # 3. 计算总资产（包含未清仓的持仓）
        final_portfolio = backtest_result['final_balance'] + \
                          backtest_result['final_holdings'] * kline_df['c'].iloc[-1]
        total_return = (final_portfolio - initial_balance) / initial_balance

        performance = evaluate_performance(backtest_result)

        # 4. 记录结果
        return {
            'short_window': short,
            'long_window': long_,
            'buy_ratio': buy_ratio,
            'sell_ratio': sell_ratio,
            'total_return': total_return,
            'final_portfolio': final_portfolio,
            'trade_count': len(backtest_result['trade_history']),
            'max_drawdown': performance['max_drawdown'],
            'win_rate': performance['win_rate'],
            'avg_return': performance['avg_return']
        }

    except Exception as e:
        if verbose:
            print(f"进程 {os.getpid()}: 参数组合 {params} 回测失败: {str(e)}")
        return None


def optimize_trading_params(kline_df, param_ranges, initial_balance=100000, fees=(0.001, 0.001),
                            verbose=True, max_workers=None):
    """
    遍历参数组合，寻找最优交易参数（使用多进程加速）

    :param kline_df: 解析后的K线数据
    :param param_ranges: 待优化参数及其取值范围
    :param initial_balance: 初始资金
    :param fees: 手续费率元组 (buy_fee_rate, sell_fee_rate)
    :param verbose: 是否打印详细日志
    :param max_workers: 进程池最大工作进程数，默认使用CPU核心数
    :return: 按总收益率排序的参数组合结果
    """
    buy_fee_rate, sell_fee_rate = fees
    results = []
    param_names = list(param_ranges.keys())
    param_values = [param_ranges[name] for name in param_names]
    param_combinations = list(itertools.product(*param_values))
    total_combinations = len(param_combinations)
    start_time = time.time()
    processed_count = multiprocessing.Value('i', 0)  # 进程安全的计数器

    if verbose:
        print(f"开始参数优化，共{total_combinations}种参数组合需要测试")
        print("=" * 60)

    # 创建进程池
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_params = {
            executor.submit(
                process_single_param_combination,
                kline_df.copy(),  # 每个进程使用数据副本
                params,
                initial_balance,
                fees,
                verbose
            ): params
            for params in param_combinations
        }

        # 处理完成的任务
        for future in as_completed(future_to_params):
            params = future_to_params[future]
            try:
                result = future.result()
                if result:
                    results.append(result)

                # 更新进度
                with processed_count.get_lock():
                    processed_count.value += 1
                    if verbose and (processed_count.value % max(1, total_combinations // 20) == 0):
                        elapsed = time.time() - start_time
                        eta = elapsed * (
                                    total_combinations - processed_count.value) / processed_count.value if processed_count.value > 0 else 0
                        print(
                            f"进度: {processed_count.value}/{total_combinations} | 已耗时: {elapsed:.1f}s | 预计剩余: {eta:.1f}s")

            except Exception as e:
                if verbose:
                    print(f"执行参数组合 {params} 时发生错误: {str(e)}")

    if verbose:
        total_time = time.time() - start_time
        print(f"参数优化完成！共耗时: {total_time:.1f}s")
        print(f"有效参数组合: {len(results)}/{total_combinations}")

    # 按总收益率降序排序
    if results:
        results_df = pd.DataFrame(results).sort_values(by='total_return', ascending=False)
        return results_df
    else:
        print("警告: 所有参数组合均失败，返回空结果")
        return pd.DataFrame()