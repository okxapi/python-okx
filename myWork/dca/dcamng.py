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
from myWork.dca.save import run_strategy
from myWork.dca.stg import DCAStrategy


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
        'price_drop_threshold': [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.05],  # 价格下跌1-5%
        'max_time_since_last_trade': [24, 48, 72, 96, 120],  # 最长无交易时间1-5小时
        'min_time_since_last_trade': [6, 12, 24, 36, 48],  # 最短无交易时间0.25-2小时
        'take_profit_threshold': [0.005, 0.01, 0.015, 0.02],  # 止盈阈值0.5-2%
        'initial_investment_ratio': [0.05, 0.1, 0.015, 0.2, 0.025, 0.3],  # 初始投资比例
        'initial_dca_value': [0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.07]  # 初始DCA值
    }

    # 初始资金通常不作为优化参数，但可以测试不同的值
    # 这里我们保持初始资金不变

    # 执行参数范围训练 (使用4个CPU核心并行处理)
    parameter_range_training(db_config, base_strategy_config, parameter_ranges, start_time, end_time, n_jobs=4)


if __name__ == "__main__":
    main()
