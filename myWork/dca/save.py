import pymysql


def save_strategy_performance(db_config, performance, strategy_config, start_time, end_time):
    """
    将策略回测结果和配置参数保存到MySQL数据库
    """
    try:
        # 连接数据库
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )

        with connection.cursor() as cursor:
            # SQL插入语句
            sql = """
            INSERT INTO strategy_performance 
            (total_return, annualized_return, sharpe_ratio, max_drawdown, 
             trade_count, dca_count, take_profit_count, win_rate, final_portfolio_value,
             price_drop_threshold, max_time_since_last_trade, min_time_since_last_trade,
             take_profit_threshold, initial_capital, initial_investment_ratio, initial_dca_value,
             start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 执行插入
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
                start_time,
                end_time
            ))

        # 提交事务
        connection.commit()
        print("策略表现数据已成功保存到数据库")

    except Exception as e:
        print(f"保存数据到数据库时出错: {e}")
    finally:
        # 关闭连接
        if connection:
            connection.close()