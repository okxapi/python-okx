import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pymysql
import random


class MySQLDataReader:
    def __init__(self, host, user, password, database, port=3306, charset='utf8mb4'):
        """
        初始化数据库连接参数

        参数:
        host: 数据库主机地址
        user: 数据库用户名
        password: 数据库密码
        database: 数据库名称
        port: 数据库端口，默认为3306
        charset: 字符集，默认为utf8mb4
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"成功连接到数据库: {self.database}")
        except Exception as e:
            print(f"连接数据库失败: {e}")
            raise

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            print("已断开数据库连接")

    def execute_query(self, query, params=None):
        """执行SQL查询并返回结果"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"执行查询失败: {e}")
            raise

    def get_sorted_history_data(self, start_time=None, end_time=None, limit=None):
        """
        获取sorted_history表中的数据

        参数:
        start_time: 开始时间，默认为None，表示不限制
        end_time: 结束时间，默认为None，表示不限制
        limit: 返回记录数限制，默认为None，表示不限制

        返回:
        pandas DataFrame格式的数据
        """
        query = "SELECT * FROM sorted_history"
        conditions = []
        params = []

        if start_time:
            conditions.append("ts >= %s")
            params.append(start_time)

        if end_time:
            conditions.append("ts <= %s")
            params.append(end_time)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY ts ASC"

        if limit:
            query += f" LIMIT {limit}"

        result = self.execute_query(query, params)

        # 转换为DataFrame
        df = pd.DataFrame(result)

        # 确保ts列是datetime类型
        if 'ts' in df.columns:
            df['ts'] = pd.to_datetime(df['ts'])

        return df


class DCAStrategy:
    def __init__(self, price_drop_threshold=0.02, max_time_since_last_trade=7,
                 min_time_since_last_trade=3, take_profit_threshold=0.01,
                 initial_capital=100000, dca_allocation_ratio=0.1):
        """
        初始化DCA策略参数

        参数:
        price_drop_threshold: 价格下跌触发DCA的阈值(百分比)
        max_time_since_last_trade: 最长无交易时间触发DCA(小时)
        min_time_since_last_trade: 最短无交易时间触发DCA(小时)
        take_profit_threshold: 止盈阈值(百分比)
        initial_capital: 初始资金
        dca_allocation_ratio: 每次DCA使用的资金比例
        """
        self.price_drop_threshold = price_drop_threshold
        self.max_time_since_last_trade = max_time_since_last_trade
        self.min_time_since_last_trade = min_time_since_last_trade
        self.take_profit_threshold = take_profit_threshold
        self.initial_capital = initial_capital
        self.dca_allocation_ratio = dca_allocation_ratio

        # 策略状态
        self.positions = []  # 持仓记录
        self.trades = []  # 交易记录
        self.portfolio = {
            'cash': initial_capital,
            'position': 0,
            'avg_price': 0,
            'last_trade_time': None,
            'peak_value': initial_capital
        }

    def prepare_data(self, df):
        """准备策略所需的数据"""
        # 确保数据按时间排序
        df = df.sort_values('ts')

        # 计算价格变动百分比
        df['price_change_pct'] = df['close'].pct_change()

        return df.dropna()

    def backtest(self, df):
        """回测策略"""
        df = self.prepare_data(df)

        # 记录每日资产变化
        portfolio_values = []
        dates = []

        # 初始化上次交易价格为第一个价格点
        self.portfolio['last_trade_price'] = df['close'].iloc[0]

        for i, row in df.iterrows():
            current_price = row['close']
            current_time = row['ts']

            # 记录日期和当前资产价值
            dates.append(current_time)
            portfolio_value = self.portfolio['cash'] + self.portfolio['position'] * current_price
            portfolio_values.append(portfolio_value)

            # 更新峰值价值
            if portfolio_value > self.portfolio['peak_value']:
                self.portfolio['peak_value'] = portfolio_value

            # 执行交易逻辑
            self._execute_trading_logic(current_time, current_price)

        # 转换为DataFrame以便分析
        self.portfolio_df = pd.DataFrame({
            'date': dates,
            'portfolio_value': portfolio_values
        })

        return self.calculate_performance(df)

    def _execute_trading_logic(self, current_time, current_price):
        """执行交易逻辑"""
        # 如果没有持仓，创建初始仓位
        if self.portfolio['position'] == 0:
            # 使用50%的资金建立初始仓位
            amount_to_invest = self.portfolio['cash'] * 0.2
            shares_to_buy = amount_to_invest / current_price

            self.portfolio['cash'] -= amount_to_invest
            self.portfolio['position'] = shares_to_buy
            self.portfolio['avg_price'] = current_price
            self.portfolio['last_trade_time'] = current_time

            self.trades.append({
                'time': current_time,
                'type': 'INITIAL_BUY',
                'price': current_price,
                'position': shares_to_buy,
                'cash': self.portfolio['cash'],
                'portfolio_value': self.portfolio['cash'] + self.portfolio['position'] * current_price
            })

            return

        # 检查是否满足止盈条件
        if self._should_take_profit(current_price):
            self._execute_take_profit(current_time, current_price)
            return

        # 检查是否满足DCA条件
        if self._should_dca(current_time, current_price):
            self._execute_dca(current_time, current_price)
            return

    def _should_take_profit(self, current_price):
        """判断是否应该止盈"""
        # 计算当前持仓的收益率
        current_return = (current_price / self.portfolio['avg_price']) - 1

        # 如果收益率达到或超过止盈阈值，则止盈
        return current_return >= self.take_profit_threshold

    def _should_dca(self, current_time, current_price):
        """判断是否应该执行DCA"""
        # 计算价格下跌幅度
        price_drop = (self.portfolio['last_trade_price'] / current_price) - 1

        # 计算自上次交易以来的时间(小时)
        if self.portfolio['last_trade_time']:
            time_since_last_trade = (current_time - self.portfolio['last_trade_time']).total_seconds() / 3600
        else:
            time_since_last_trade = float('inf')

        # 随机选择一个介于min和max之间的时间阈值
        random_time_threshold = random.uniform(self.min_time_since_last_trade, self.max_time_since_last_trade)

        # 如果价格下跌超过阈值或者无交易时间超过随机时间阈值，则执行DCA
        return (price_drop >= self.price_drop_threshold) or (time_since_last_trade >= random_time_threshold)

    def _execute_take_profit(self, current_time, current_price):
        """执行止盈操作"""
        # 卖出全部持仓
        position_value = self.portfolio['position'] * current_price
        profit = position_value - (self.portfolio['position'] * self.portfolio['avg_price'])

        self.portfolio['cash'] += position_value
        self.portfolio['position'] = 0
        self.portfolio['avg_price'] = 0
        self.portfolio['last_trade_time'] = current_time
        self.portfolio['last_trade_price'] = current_price

        self.trades.append({
            'time': current_time,
            'type': 'TAKE_PROFIT',
            'price': current_price,
            'position': 0,
            'cash': self.portfolio['cash'],
            'profit': profit,
            'portfolio_value': self.portfolio['cash']
        })

    def _execute_dca(self, current_time, current_price):
        """执行DCA操作"""
        # 计算可用资金并使用设定比例进行DCA
        amount_to_invest = self.portfolio['cash'] * self.dca_allocation_ratio
        shares_to_buy = amount_to_invest / current_price

        # 更新平均价格
        total_value = (self.portfolio['position'] * self.portfolio['avg_price']) + amount_to_invest
        total_shares = self.portfolio['position'] + shares_to_buy
        new_avg_price = total_value / total_shares

        # 更新投资组合
        self.portfolio['cash'] -= amount_to_invest
        self.portfolio['position'] = total_shares
        self.portfolio['avg_price'] = new_avg_price
        self.portfolio['last_trade_time'] = current_time
        self.portfolio['last_trade_price'] = current_price

        self.trades.append({
            'time': current_time,
            'type': 'DCA',
            'price': current_price,
            'position': total_shares,
            'cash': self.portfolio['cash'],
            'avg_price': new_avg_price,
            'portfolio_value': self.portfolio['cash'] + total_shares * current_price
        })

    def calculate_performance(self, df):
        """计算策略表现指标"""
        if not hasattr(self, 'portfolio_df'):
            return "请先运行回测"

        # 计算每日收益率
        self.portfolio_df['daily_return'] = self.portfolio_df['portfolio_value'].pct_change()

        # 计算累计收益率
        total_return = (self.portfolio_df['portfolio_value'].iloc[-1] /
                        self.portfolio_df['portfolio_value'].iloc[0] - 1)

        # 计算年化收益率
        days = (self.portfolio_df['date'].iloc[-1] - self.portfolio_df['date'].iloc[0]).days
        annualized_return = (1 + total_return) ** (365 / days) - 1 if days > 0 else 0

        # 计算夏普比率
        risk_free_rate = 0.03  # 假设无风险利率为3%
        daily_risk_free = (1 + risk_free_rate) ** (1 / 365) - 1
        excess_returns = self.portfolio_df['daily_return'] - daily_risk_free
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else 0

        # 计算最大回撤
        self.portfolio_df['cum_max'] = self.portfolio_df['portfolio_value'].cummax()
        self.portfolio_df['drawdown'] = self.portfolio_df['portfolio_value'] / self.portfolio_df['cum_max'] - 1
        max_drawdown = self.portfolio_df['drawdown'].min()

        # 计算交易次数和胜率
        trade_count = len([t for t in self.trades if t['type'] in ['TAKE_PROFIT', 'DCA', 'INITIAL_BUY']])
        take_profit_trades = [t for t in self.trades if t['type'] == 'TAKE_PROFIT']
        winning_trades = [t for t in take_profit_trades if 'profit' in t and t['profit'] > 0]
        win_rate = len(winning_trades) / len(take_profit_trades) if len(take_profit_trades) > 0 else 0

        # 计算DCA使用次数
        dca_count = len([t for t in self.trades if t['type'] == 'DCA'])

        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'trade_count': trade_count,
            'dca_count': dca_count,
            'take_profit_count': len(take_profit_trades),
            'win_rate': win_rate,
            'final_portfolio_value': self.portfolio_df['portfolio_value'].iloc[-1]
        }

    def plot_performance(self):
        """绘制策略表现图表"""
        if not hasattr(self, 'portfolio_df'):
            print("请先运行回测")
            return

        plt.figure(figsize=(14, 10))

        # 绘制资产曲线
        plt.subplot(3, 1, 1)
        plt.plot(self.portfolio_df['date'], self.portfolio_df['portfolio_value'])
        plt.title('Portfolio Value Over Time')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.grid(True)

        # 绘制回撤曲线
        plt.subplot(3, 1, 2)
        plt.fill_between(self.portfolio_df['date'], self.portfolio_df['drawdown'], 0,
                         color='red', alpha=0.3)
        plt.title('Drawdown Over Time')
        plt.xlabel('Date')
        plt.ylabel('Drawdown (%)')
        plt.grid(True)

        # 绘制交易点
        plt.subplot(3, 1, 3)
        trade_dates = [t['time'] for t in self.trades]
        trade_prices = [t['price'] for t in self.trades]
        trade_types = [t['type'] for t in self.trades]

        buy_dates = [trade_dates[i] for i in range(len(trade_dates)) if trade_types[i] in ['INITIAL_BUY', 'DCA']]
        buy_prices = [trade_prices[i] for i in range(len(trade_prices)) if trade_types[i] in ['INITIAL_BUY', 'DCA']]

        sell_dates = [trade_dates[i] for i in range(len(trade_dates)) if trade_types[i] == 'TAKE_PROFIT']
        sell_prices = [trade_prices[i] for i in range(len(trade_prices)) if trade_types[i] == 'TAKE_PROFIT']

        plt.plot(self.portfolio_df['date'], self.portfolio_df['portfolio_value'], label='Portfolio Value')
        plt.scatter(buy_dates,
                    [self.portfolio_df[self.portfolio_df['date'] == d]['portfolio_value'].values[0] for d in buy_dates],
                    color='green', marker='^', s=100, label='Buy')
        plt.scatter(sell_dates, [self.portfolio_df[self.portfolio_df['date'] == d]['portfolio_value'].values[0] for d in
                                 sell_dates],
                    color='red', marker='v', s=100, label='Sell')

        plt.title('Trading Points')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()


# 主函数：整合数据库读取和策略回测
def main():
    # 配置数据库连接信息
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'qwe12345',
        'database': 'trading_db',
        'port': 3306
    }

    # 配置策略参数
    strategy_config = {
        'price_drop_threshold': 0.02,  # 价格下跌2%触发DCA
        'max_time_since_last_trade': 7,  # 最长7小时无交易触发DCA
        'min_time_since_last_trade': 3,  # 最短3小时无交易触发DCA
        'take_profit_threshold': 0.01,  # 1%止盈
        'initial_capital': 100000,  # 初始资金100,000
        'dca_allocation_ratio': 0.05  # 每次DCA使用10%资金
    }

    # 配置数据时间范围
    end_time = datetime.now()
    start_time = end_time - pd.Timedelta(days=365)  # 获取最近30天的数据

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

        # 绘制表现图表
        strategy.plot_performance()

        # 打印最近10笔交易
        print("\n最近10笔交易:")
        for trade in strategy.trades[-100:]:
            if(trade['type'] == 'TAKE_PROFIT') or (trade['type'] == 'INITIAL_BUY'):
                print(f"{trade['time']} - {trade['type']}: {trade['position']} units at {trade['price']}")

    except Exception as e:
        print(f"运行策略时发生错误: {e}")


if __name__ == "__main__":
    main()