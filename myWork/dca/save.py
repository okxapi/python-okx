import pymysql

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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)
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
                performance.get('total_fees', 0),
                start_time,
                end_time
            ))
        connection.commit()
        print("\n数据已成功提交到数据库")

    except Exception as e:
        print(f"\n保存数据到数据库时出错: {e}")
        import traceback
        traceback.print_exc()
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