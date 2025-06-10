import datetime
from functools import partial
from itertools import product
from multiprocessing import Pool

import numpy as np
import pandas as pd
from tqdm import tqdm

from myWork.dca.test.mysql_read import MySQLDataReader
from myWork.dca.test.save import run_strategy_df


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

    reader = MySQLDataReader(**db_config)
    reader.connect()
    df = reader.get_sorted_history_data(start_time, end_time, config.get('currency', 'UNKNOWN'))
    reader.disconnect()

    # 使用多进程并行运行回测
    with Pool(processes=n_jobs) as pool:
        func = partial(run_strategy_df, db_config=db_config,
                       start_time=start_time, end_time=end_time, df=df)
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
        'host': '192.168.123.11',
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
        'initial_dca_value': 0.035,  # 初始DCA值
        # 'currency':"SUI"
    }

    # 配置数据时间范围
    end_time = datetime.datetime(2025, 6, 8)  # 设置结束时间为2025年6月8日
    start_time = end_time - pd.Timedelta(days=120)  # 开始时间为结束时间前120天

    # 定义要测试的参数范围
    def generate_range(min_val, max_val, step):
        """生成从min到max的等间隔数值列表"""
        return list(np.arange(min_val, max_val + step, step))

    parameter_ranges = {
        'price_drop_threshold': generate_range(0.01, 0.05, 0.005),  # 价格下跌1-5%
        'max_time_since_last_trade': generate_range(24, 120, 24),  # 最长无交易时间1-5天
        'min_time_since_last_trade': generate_range(6, 48, 6),  # 最短无交易时间0.25-2天
        'take_profit_threshold': generate_range(0.005, 0.03, 0.005),  # 止盈阈值0.5-2%
        'initial_investment_ratio': generate_range(0.05, 0.3, 0.05),  # 初始投资比例5-30%
        'initial_dca_value': generate_range(0.02, 0.06
                                            , 0.005)  # 初始DCA值2-7%
    }

    # 初始资金通常不作为优化参数，但可以测试不同的值
    # 这里我们保持初始资金不变

    # 执行参数范围训练 (使用4个CPU核心并行处理)
    parameter_range_training(db_config, base_strategy_config, parameter_ranges, start_time, end_time, n_jobs=8)


if __name__ == "__main__":
    main()
