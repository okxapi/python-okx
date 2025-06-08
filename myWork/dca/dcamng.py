import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pymysql
import random

from myWork.dca.mysql_read import MySQLDataReader
from myWork.dca.save import save_strategy_performance
from myWork.dca.stg import DCAStrategy

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'qwe12345',
    'database': 'trading_db',
    'port': 3306
}

# 主函数：整合数据库读取和策略回测
def main():
    # 配置数据库连接信息


    # 配置策略参数
    strategy_config = {
        'price_drop_threshold': 0.02,  # 价格下跌2%触发DCA
        'max_time_since_last_trade': 96,  # 最长7小时无交易触发DCA
        'min_time_since_last_trade': 24,  # 最短3小时无交易触发DCA
        'take_profit_threshold': 0.01,  # 1%止盈
        'initial_capital': 100000,  # 初始资金100,000
        'initial_investment_ratio': 0.1,  # 初始投资使用50%资金
        'initial_dca_value': 0.035
    }

    # 配置数据时间范围
    end_time = datetime.now()
    start_time = end_time - pd.Timedelta(days=90)  # 获取最近30天的数据

    try:
        # 创建数据读取器实例
        reader = MySQLDataReader(**db_config)

        # 连接数据库并获取数据
        reader.connect()
        print(f"正在获取 {start_time} 到 {end_time} 的交易数据...")
        df = reader.get_sorted_history_data(start_time, end_time)
        reader.disconnect()

        if df.empty:
            print("未获取到任何数据，请检查数据库连接和查询条件")
            return

        print(f"成功获取 {len(df)} 条记录")

        # 创建并运行策略
        strategy = DCAStrategy(**strategy_config)
        performance = strategy.backtest(df)

        # 打印策略表现
        print("\n策略表现:")
        for key, value in performance.items():
            print(f"{key}: {value}")

        if performance:
            save_strategy_performance(db_config, performance, strategy_config, start_time, end_time)

        # # 打印首次DCA金额和后续DCA记录
        # if strategy.initial_dca_amount is not None:
        #     print(f"\n首次DCA金额: {strategy.initial_dca_amount}")
        #
        #     dca_trades = [t for t in strategy.trades if t['type'] == 'DCA']
        #     print(f"DCA操作次数: {len(dca_trades)}")
        #
        #     if dca_trades:
        #         print("\nDCA操作明细:")
        #         for i, trade in enumerate(dca_trades):
        #             print(f"DCA #{i + 1}: {trade['time']} - 金额: {trade['dca_amount']}, 价格: {trade['price']}")

        # 绘制表现图表
        # strategy.plot_performance()

    except Exception as e:
        print(f"运行策略时发生错误: {e}")



if __name__ == "__main__":
    main()
