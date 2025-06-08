import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pymysql
import random
from itertools import product
from multiprocessing import Pool
from functools import partial
from tqdm import tqdm
from myWork.dca.mysql_read import MySQLDataReader
from myWork.dca.stg import DCAStrategy


def save_strategy_performance(db_config, performance, strategy_config, start_time, end_time):
    """将策略回测结果和配置参数保存到MySQL数据库"""
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO strategy_performance 
            (total_return, annualized_return, sharpe_ratio, max_drawdown, 
             trade_count, dca_count, take_profit_count, win_rate, final_portfolio_value,
             price_drop_threshold, max_time_since_last_trade, min_time_since_last_trade,
             take_profit_threshold, initial_capital, initial_investment_ratio, initial_dca_value,
             total_fees,
             start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s，%s)
            """
            cursor.execute(sql, (
                performance['total_return'],
                performance['annualized_return'],
                performance['sharpe_ratio'],
                performance['max_drawdown'],
                performance['trade_count'],
                performance['dca_count'],
                performance['take_profit_count'],
                performance['win_rate'],
                performance['final_portfolio_value'],
                strategy_config['price_drop_threshold'],
                strategy_config['max_time_since_last_trade'],
                strategy_config['min_time_since_last_trade'],
                strategy_config['take_profit_threshold'],
                strategy_config['initial_capital'],
                strategy_config['initial_investment_ratio'],
                strategy_config['initial_dca_value'],
                performance['total_fees'],
                start_time,
                end_time
            ))
        connection.commit()
    except Exception as e:
        print(f"保存数据到数据库时出错: {e}")
    finally:
        if connection:
            connection.close()


def run_strategy(config, db_config, start_time, end_time):
    """运行策略并返回性能指标"""
    try:
        reader = MySQLDataReader(**db_config)
        reader.connect()
        df = reader.get_sorted_history_data(start_time, end_time)
        reader.disconnect()

        if df.empty:
            print("未获取到任何数据")
            return None

        strategy = DCAStrategy(**config)
        performance = strategy.backtest(df)

        # 保存到数据库
        save_strategy_performance(db_config, performance, config, start_time, end_time)

        return {
            'config': config,
            'performance': performance
        }
    except Exception as e:
        print(f"运行策略时发生错误: {e}")
        return None


def parameter_range_training(db_config, base_config, param_ranges, start_time, end_time, n_jobs=1):
    """
    执行参数范围训练，测试不同参数组合的策略表现

    参数:
    db_config - 数据库连接配置
    base_config - 基础策略配置
    param_ranges - 要测试的参数范围字典
    start_time, end_time - 回测时间范围
    n_jobs - 并行处理数
    """
    # 生成所有参数组合
    param_names = list(param_ranges.keys())
    param_values = list(param_ranges.values())
    param_combinations = list(product(*param_values))

    total_runs = len(param_combinations)
    print(f"开始参数范围训练，共{total_runs}次回测")

    # 创建所有配置组合
    all_configs = []
    for params in param_combinations:
        config = base_config.copy()
        for name, value in zip(param_names, params):
            config[name] = value
        all_configs.append(config)

    # 使用多进程并行运行回测
    with Pool(processes=n_jobs) as pool:
        func = partial(run_strategy, db_config=db_config,
                       start_time=start_time, end_time=end_time)
        results = list(tqdm(pool.imap(func, all_configs), total=total_runs))

    # 过滤掉失败的结果
    valid_results = [r for r in results if r is not None]

    if not valid_results:
        print("没有成功完成的回测")
        return

    # 找出最佳参数组合（基于夏普比率）
    best_result = max(valid_results, key=lambda x: x['performance']['sharpe_ratio'])

    print("\n参数训练完成!")
    print("最佳参数配置:")
    for key, value in best_result['config'].items():
        print(f"{key}: {value}")

    print("\n最佳策略表现:")
    for key, value in best_result['performance'].items():
        print(f"{key}: {value}")


def main():
    # 配置数据库连接信息
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'qwe12345',
        'database': 'trading_db',
        'port': 3306
    }

    # 基础策略配置
    base_strategy_config = {
        'price_drop_threshold': 0.02,  # 价格下跌触发DCA的阈值
        'max_time_since_last_trade': 96,  # 最长无交易时间触发DCA (4小时)
        'min_time_since_last_trade': 24,  # 最短无交易时间触发DCA (1小时)
        'take_profit_threshold': 0.01,  # 止盈阈值
        'initial_capital': 100000,  # 初始资金
        'initial_investment_ratio': 0.1,  # 初始投资比例
        'initial_dca_value': 0.035  # 初始DCA值
    }

    # 配置数据时间范围
    end_time = datetime.now()
    start_time = end_time - pd.Timedelta(days=90)

    # 定义要测试的参数范围
    parameter_ranges = {
        'price_drop_threshold': [0.01, 0.02, 0.03, 0.05],  # 价格下跌1-5%
        'max_time_since_last_trade': [24, 48, 72, 96, 120],  # 最长无交易时间1-5小时
        'min_time_since_last_trade': [6, 12, 24, 48],  # 最短无交易时间0.25-2小时
        'take_profit_threshold': [0.005, 0.01, 0.015, 0.02],  # 止盈阈值0.5-2%
        'initial_investment_ratio': [0.05, 0.1, 0.2, 0.3],  # 初始投资比例
        'initial_dca_value': [0.02, 0.035, 0.05, 0.07]  # 初始DCA值
    }

    # 初始资金通常不作为优化参数，但可以测试不同的值
    # 这里我们保持初始资金不变

    # 执行参数范围训练 (使用4个CPU核心并行处理)
    parameter_range_training(db_config, base_strategy_config, parameter_ranges, start_time, end_time, n_jobs=1)


if __name__ == "__main__":
    main()