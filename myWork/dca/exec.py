import os
import random
import time
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict, Optional

import pymysql
from dotenv import load_dotenv
from okx import MarketData, PublicData
from okx.Trade import TradeAPI

from myWork.another.all import get_instrument_info, get_realtime_price

# 初始化API客户端
load_dotenv()
api_key = os.getenv("OKX_API_KEY")
api_secret_key = os.getenv("OKX_API_SECRET")
passphrase = os.getenv("OKX_API_PASSPHRASE")
ENV_FLAG = os.getenv("OKX_ENV_FLAG")

# API实例
trade_api = TradeAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag=ENV_FLAG)
market_api = MarketData.MarketAPI(flag=ENV_FLAG)
public_api = PublicData.PublicAPI(flag=ENV_FLAG)


class DcaExeStrategy:
    def __init__(self, price_drop_threshold=0.02, max_time_since_last_trade=7,
                 min_time_since_last_trade=3, take_profit_threshold=0.01,
                 initial_capital=100000, initial_investment_ratio=0.5, initial_dca_value=0.1,
                 buy_fee_rate=0.001, sell_fee_rate=0.001):
        """
        初始化DCA策略参数

        参数:
        price_drop_threshold: 价格下跌触发DCA的阈值(百分比)
        max_time_since_last_trade: 最长无交易时间触发DCA(小时)
        min_time_since_last_trade: 最短无交易时间触发DCA(小时)
        take_profit_threshold: 止盈阈值(百分比)
        initial_capital: 初始资金
        initial_investment_ratio: 初始投资使用的资金比例
        buy_fee_rate: 买入交易费用比例
        sell_fee_rate: 卖出交易费用比例
        """
        self.price_drop_threshold = price_drop_threshold
        self.max_time_since_last_trade = max_time_since_last_trade
        self.min_time_since_last_trade = min_time_since_last_trade
        self.take_profit_threshold = take_profit_threshold
        self.initial_capital = initial_capital
        self.initial_investment_ratio = initial_investment_ratio
        self.initial_dca_value = initial_dca_value
        self.buy_fee_rate = buy_fee_rate
        self.sell_fee_rate = sell_fee_rate

        # 策略状态
        self.positions = []  # 持仓记录
        self.trades = []  # 交易记录
        self.portfolio = {
            'cash': initial_capital,
            'position': 0,
            'avg_price': 0,
            'last_trade_time': None,
            'last_trade_price': None,
            'peak_value': initial_capital
        }
        self.initial_dca_amount = None  # 记录首次DCA金额

    def execute_logic(self, current_time, current_price):
        """执行交易逻辑并返回交易决策"""
        # 如果没有持仓，创建初始仓位
        if self.portfolio['position'] == 0:
            return self._create_initial_position(current_time, current_price)

        # 检查是否满足止盈条件
        if self._should_take_profit(current_price):
            return self._create_take_profit_order(current_time, current_price)

        # 检查是否满足DCA条件
        if self._should_dca(current_time, current_price):
            return self._create_dca_order(current_time, current_price)

        return None

    def _create_initial_position(self, current_time, current_price):
        """创建初始仓位"""
        # 使用设定比例的资金建立初始仓位
        amount_to_invest = self.portfolio['cash'] * self.initial_investment_ratio

        # 计算包含交易费用的总金额
        total_amount = amount_to_invest / (1 - self.buy_fee_rate)

        # 计算实际支付的交易费用
        fee = total_amount - amount_to_invest

        # 计算可购买的份额
        shares_to_buy = amount_to_invest / current_price

        # 记录交易信息
        trade_info = {
            'time': current_time,
            'type': 'INITIAL_BUY',
            'price': current_price,
            'position': shares_to_buy,
            'cash': self.portfolio['cash'] - total_amount,
            'portfolio_value': self.portfolio['cash'] + self.portfolio['position'] * current_price,
            'fee': fee,
            'amount': total_amount,
            'side': 'buy'
        }

        # 更新投资组合
        self.portfolio['cash'] -= total_amount
        self.portfolio['position'] = shares_to_buy
        self.portfolio['avg_price'] = current_price
        self.portfolio['last_trade_time'] = current_time
        self.portfolio['last_trade_price'] = current_price

        # 记录首次DCA金额(初始买入后第一次DCA的金额)
        self.initial_dca_amount = None

        self.trades.append(trade_info)
        return trade_info

    def _should_take_profit(self, current_price):
        """判断是否应该止盈"""
        # 计算当前持仓的收益率
        if self.portfolio['avg_price'] == 0:
            return False

        current_return = (current_price / self.portfolio['avg_price']) - 1

        # 如果收益率达到或超过止盈阈值，则止盈
        return current_return >= self.take_profit_threshold

    def _should_dca(self, current_time, current_price):
        """判断是否应该执行DCA"""
        if self.portfolio['last_trade_price'] is None:
            return False

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

    def _create_dca_order(self, current_time, current_price):
        """创建DCA订单"""
        # 首次DCA时记录金额
        if self.initial_dca_amount is None:
            # 使用剩余资金的一定比例作为首次DCA金额
            self.initial_dca_amount = self.portfolio['cash'] * self.initial_dca_value

        # 确保有足够的资金进行DCA
        if self.portfolio['cash'] < self.initial_dca_amount:
            # 如果资金不足，使用所有剩余资金
            amount_to_invest = self.portfolio['cash']
            if amount_to_invest <= 0:
                return None
        else:
            amount_to_invest = self.initial_dca_amount

        # 计算包含交易费用的总金额
        total_amount = amount_to_invest / (1 - self.buy_fee_rate)

        # 计算实际支付的交易费用
        fee = total_amount - amount_to_invest

        # 计算可购买的份额
        shares_to_buy = amount_to_invest / current_price

        # 更新平均价格
        total_value = (self.portfolio['position'] * self.portfolio['avg_price']) + total_amount
        total_shares = self.portfolio['position'] + shares_to_buy
        new_avg_price = total_value / total_shares

        # 记录交易信息
        trade_info = {
            'time': current_time,
            'type': 'DCA',
            'price': current_price,
            'position': total_shares,
            'cash': self.portfolio['cash'] - total_amount,
            'avg_price': new_avg_price,
            'portfolio_value': self.portfolio['cash'] + total_shares * current_price,
            'dca_amount': amount_to_invest,
            'fee': fee,
            'amount': total_amount,
            'side': 'buy'
        }

        # 更新投资组合
        self.portfolio['cash'] -= total_amount
        self.portfolio['position'] = total_shares
        self.portfolio['avg_price'] = new_avg_price
        self.portfolio['last_trade_time'] = current_time
        self.portfolio['last_trade_price'] = current_price

        self.trades.append(trade_info)
        return trade_info

    def _create_take_profit_order(self, current_time, current_price):
        """创建止盈订单"""
        # 计算持仓价值
        position_value = self.portfolio['position'] * current_price

        # 计算交易费用
        fee = position_value * self.sell_fee_rate

        # 计算扣除交易费用后的实际收入
        actual_income = position_value - fee

        # 计算利润
        profit = actual_income - (self.portfolio['position'] * self.portfolio['avg_price'])

        # 记录交易信息
        trade_info = {
            'time': current_time,
            'type': 'TAKE_PROFIT',
            'price': current_price,
            'position': 0,
            'cash': self.portfolio['cash'] + actual_income,
            'profit': profit,
            'portfolio_value': self.portfolio['cash'] + actual_income,
            'fee': fee,
            'amount': position_value,
            'side': 'sell'
        }

        # 更新投资组合
        self.portfolio['cash'] += actual_income
        self.portfolio['position'] = 0
        self.portfolio['avg_price'] = 0
        self.portfolio['last_trade_time'] = current_time
        self.portfolio['last_trade_price'] = current_price

        self.trades.append(trade_info)
        return trade_info


class DatabaseManager:
    """数据库管理类，负责交易数据的存储"""

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
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
                cursorclass=pymysql.cursors.DictCursor
            )
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            raise

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")

    def create_tables(self):
        """创建交易数据表"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                # 创建交易记录表
                create_trades_table = """
                CREATE TABLE IF NOT EXISTS trades (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    inst_id VARCHAR(50) NOT NULL,
                    trade_time DATETIME NOT NULL,
                    trade_type ENUM('INITIAL_BUY', 'DCA', 'TAKE_PROFIT') NOT NULL,
                    price DECIMAL(20, 8) NOT NULL,
                    amount DECIMAL(20, 8) NOT NULL,
                    position DECIMAL(20, 8) NOT NULL,
                    cash DECIMAL(20, 8) NOT NULL,
                    fee DECIMAL(20, 8) NOT NULL,
                    profit DECIMAL(20, 8),
                    dca_amount DECIMAL(20, 8),
                    avg_price DECIMAL(20, 8),
                    portfolio_value DECIMAL(20, 8) NOT NULL,
                    side ENUM('buy', 'sell') NOT NULL,
                    order_id VARCHAR(50),
                    status ENUM('pending', 'filled', 'cancelled') NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_trades_table)

                # 创建持仓记录表
                create_positions_table = """
                CREATE TABLE IF NOT EXISTS positions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    inst_id VARCHAR(50) NOT NULL,
                    position DECIMAL(20, 8) NOT NULL,
                    avg_price DECIMAL(20, 8) NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_positions_table)

                # 创建订单记录表
                create_orders_table = """
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    inst_id VARCHAR(50) NOT NULL,
                    order_id VARCHAR(50) NOT NULL,
                    side ENUM('buy', 'sell') NOT NULL,
                    price DECIMAL(20, 8) NOT NULL,
                    size DECIMAL(20, 8) NOT NULL,
                    status ENUM('pending', 'filled', 'cancelled', 'rejected') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    filled_at TIMESTAMP NULL,
                    error_message TEXT
                )
                """
                cursor.execute(create_orders_table)

            self.connection.commit()
            print("数据库表创建成功")
        except Exception as e:
            print(f"创建数据库表失败: {e}")
            raise

    def record_trade(self, inst_id: str, trade_info: Dict, order_id: Optional[str] = None, status: str = 'pending'):
        """记录交易信息到数据库"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO trades (
                    inst_id, trade_time, trade_type, price, amount, position, cash, 
                    fee, profit, dca_amount, avg_price, portfolio_value, side, order_id, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # 确保所有需要的字段都存在
                profit = trade_info.get('profit', 0)
                dca_amount = trade_info.get('dca_amount', 0)
                avg_price = trade_info.get('avg_price', 0)

                cursor.execute(sql, (
                    inst_id,
                    trade_info['time'],
                    trade_info['type'],
                    trade_info['price'],
                    trade_info['amount'],
                    trade_info['position'],
                    trade_info['cash'],
                    trade_info['fee'],
                    profit,
                    dca_amount,
                    avg_price,
                    trade_info['portfolio_value'],
                    trade_info['side'],
                    order_id,
                    status
                ))

            self.connection.commit()
            print(f"交易记录已保存: {trade_info['type']} at {trade_info['price']}")
        except Exception as e:
            print(f"保存交易记录失败: {e}")
            self.connection.rollback()
            raise

    def update_order_status(self, order_id: str, status: str, error_message: Optional[str] = None):
        """更新订单状态"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                if status == 'filled':
                    sql = "UPDATE orders SET status = %s, filled_at = NOW() WHERE order_id = %s"
                    cursor.execute(sql, (status, order_id))
                else:
                    sql = "UPDATE orders SET status = %s, error_message = %s WHERE order_id = %s"
                    cursor.execute(sql, (status, error_message, order_id))

            self.connection.commit()
            print(f"订单状态已更新: {order_id} -> {status}")
        except Exception as e:
            print(f"更新订单状态失败: {e}")
            self.connection.rollback()
            raise


class TradingExecutor:
    """交易执行器，负责执行交易决策并与API交互"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def execute_trade(self, inst_id: str, trade_info: Dict) -> Optional[str]:
        """执行交易并返回订单ID"""
        # 获取产品信息
        instrument_info = get_instrument_info(inst_id)
        if not instrument_info:
            print(f"无法获取{inst_id}的产品信息，交易取消")
            return None

        # 获取最新价格
        price_data = get_realtime_price(inst_id)
        if not price_data:
            print(f"无法获取{inst_id}的最新价格，交易取消")
            return None

        # 根据交易类型确定使用买价还是卖价
        if trade_info['side'] == 'buy':
            price = price_data['ask_px']
        else:  # sell
            price = price_data['bid_px']

        # 确保价格符合精度要求
        tick_sz = float(instrument_info.get('tickSz', '0.01'))
        adjusted_px = round(price, self._get_precision(tick_sz))

        # 确定交易数量
        if trade_info['side'] == 'buy':
            # 买入时，根据金额计算数量
            min_sz = float(instrument_info.get('minSz', '0.001'))
            sz = trade_info['amount'] / adjusted_px

            # 确保数量符合最小下单量要求
            if sz < min_sz:
                print(f"计算的下单量{sz}小于最小下单量{min_sz}，交易取消")
                return None

            # 调整数量精度
            sz_precision = self._get_precision(min_sz)
            final_sz = round(sz, sz_precision)
        else:  # sell
            # 卖出时，使用当前持仓量
            final_sz = trade_info['position']

        # 构造交易参数
        trade_params = {
            "instId": inst_id,
            "tdMode": "isolated",
            "side": trade_info['side'],
            "ccy": "USDT",
            "ordType": "limit",
            "sz": f"{final_sz:.8f}",  # 数量精度
            "px": f"{adjusted_px:.8f}"  # 价格精度
        }

        # 记录初始订单
        self.db_manager.record_trade(inst_id, trade_info, status='pending')

        # 执行下单
        max_retries = 3
        order_id = None

        for attempt in range(max_retries):
            try:
                print(f"[{attempt + 1}/{max_retries}] 提交订单: {trade_params}")
                result = trade_api.place_order(**trade_params)

                if result["code"] == "0" and len(result.get("data", [])) > 0:
                    order_id = result["data"][0]["ordId"]
                    print(f"订单提交成功，订单ID: {order_id}")

                    # 更新订单状态
                    self.db_manager.update_order_status(order_id, 'filled')
                    self.db_manager.record_trade(inst_id, trade_info, order_id, 'filled')
                    break
                else:
                    error = result.get("data", [{}])[0]
                    error_msg = error.get("sMsg", "未知错误")
                    error_code = error.get("sCode", "未知代码")
                    print(f"订单失败 (代码: {error_code}): {error_msg}")

                    # 处理特定错误
                    if error_code == "51137" and "buy orders" in error_msg:
                        new_px = float(error_msg.split("is ")[1].split(". ")[0])
                        print(f"触发价格限制，使用强制限价: {new_px}")
                        trade_params["px"] = f"{new_px:.8f}"
                    else:
                        self.db_manager.update_order_status(order_id, 'rejected', error_msg)
                        break
            except Exception as e:
                print(f"下单异常: {str(e)}")
                if attempt == max_retries - 1:
                    self.db_manager.update_order_status(order_id, 'rejected', str(e))

            time.sleep(1)  # API调用间隔

        return order_id

    def _get_precision(self, value: float) -> int:
        """获取数值的小数位数精度"""
        value_str = str(value)
        if '.' in value_str:
            return len(value_str.split('.')[1])
        return 0


def main():
    """主函数，程序入口点"""
    # 配置数据库连接
    db_manager = DatabaseManager(
        host="19.168.123.11",
        user="root",
        password="qwe12345",
        database="trading_db"
    )

    # 创建数据库表
    db_manager.create_tables()

    # 初始化策略
    strategy = DcaExeStrategy(
        price_drop_threshold=0.03,  # 价格下跌3%触发DCA
        take_profit_threshold=0.02,  # 利润达到2%触发止盈
        initial_capital=100000,  # 初始资金100,000 USDT
        initial_investment_ratio=0.5,  # 初始投资使用50%的资金
        initial_dca_value=0.1  # 首次DCA使用剩余资金的10%
    )

    # 初始化交易执行器
    executor = TradingExecutor(db_manager)

    # 交易配置
    inst_id = "BTC-USDT"  # 交易对
    trading_interval = 60  # 交易检查间隔(秒)

    print(f"开始执行DCA交易策略 - 交易对: {inst_id}")

    try:
        while True:
            current_time = datetime.now()
            print(f"\n{current_time} - 检查交易信号...")

            # 获取当前价格
            price_data = get_realtime_price(inst_id)
            if not price_data:
                print("无法获取价格数据，跳过本次检查")
                time.sleep(trading_interval)
                continue

            current_price = (price_data['ask_px'] + price_data['bid_px']) / 2  # 使用中间价
            print(f"当前价格: {current_price}")

            # 执行策略逻辑
            trade_decision = strategy.execute_logic(current_time, current_price)

            if trade_decision:
                print(f"生成交易决策: {trade_decision['type']} at {trade_decision['price']}")

                # 执行交易
                order_id = executor.execute_trade(inst_id, trade_decision)
                if order_id:
                    print(f"交易执行成功，订单ID: {order_id}")
                else:
                    print("交易执行失败")
            else:
                print("无交易信号")

            # 打印当前投资组合状态
            portfolio_value = strategy.portfolio['cash'] + strategy.portfolio['position'] * current_price
            print(f"当前投资组合价值: {portfolio_value:.2f} USDT")
            print(f"现金: {strategy.portfolio['cash']:.2f} USDT")
            print(f"持仓: {strategy.portfolio['position']:.8f} {inst_id.split('-')[0]}")
            if strategy.portfolio['position'] > 0:
                print(f"平均价格: {strategy.portfolio['avg_price']:.2f} USDT")

            # 等待下一个检查周期
            time.sleep(trading_interval)

    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭数据库连接
        db_manager.disconnect()


if __name__ == "__main__":
    main()
