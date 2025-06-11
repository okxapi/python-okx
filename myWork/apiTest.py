import okx.MarketData as MarketData
import time
import datetime
import pandas as pd
import os
import json
import random
import pymysql
from dotenv import load_dotenv
from tqdm import tqdm

# ======================
# 配置参数
# ======================
CONFIG = {
    "API_ENV": "0",  # 0: 实盘, 1: 模拟盘
    "INST_ID": "SUI-USDT",  # 交易对
    "BAR": "1m",  # 时间粒度 (1s/1m/3m/5m/15m/30m/1H/2H/4H/6H/12H/1D等)
    "LIMIT": 100,  # 每页数据量 (最大100)
    "TIME_RANGE_DAYS": 1500,  # 时间范围 (天数)
    "MAX_DATA_LIMIT": 10000000,  # 最大数据量限制
    "SAVE_PATH": "./",  # 数据保存路径 (结尾带/)
    "TEMP_FILE": "temp_history.csv",  # 临时数据文件名
    "FINAL_FILE": "sorted_history.csv",  # 最终排序后文件名
    "STATE_FILE": "download_state.json",  # 状态保存文件名
    "MAX_RETRIES": 5,  # API请求最大重试次数
    "RETRY_DELAY": 5,  # 重试前等待秒数 (基础值)
    "RANDOM_DELAY": 3,  # 随机延迟上限 (避免请求风暴)
    "MYSQL_TABLE": "sorted_history_sui"  # MySQL表名
}

load_dotenv()

# 获取配置
MYSQL_CONN = os.getenv("MYSQL_CONN")
MYSQL_PASS = os.getenv("MYSQL_PASS")

# 全局数据库连接对象
connection = None


def create_connection():
    """创建与MySQL数据库的持久化连接"""
    global connection
    try:
        if connection and not connection.open:
            connection = None

        if not connection:
            connection = pymysql.connect(
                host=MYSQL_CONN,
                port=3306,
                user='root',
                password=MYSQL_PASS,
                database='trading_db',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False  # 手动管理事务
            )
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None


def create_table_if_not_exists():
    """如果表不存在，则创建表"""
    connection = create_connection()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            # 创建表的SQL语句
            sql = f"""
            CREATE TABLE IF NOT EXISTS {CONFIG['MYSQL_TABLE']} (
                ts DATETIME NOT NULL,
                open DECIMAL(30,15),
                high DECIMAL(30,15),
                low DECIMAL(30,15),
                close DECIMAL(30,15),
                volume DECIMAL(30,15),
                vol_ccy VARCHAR(50),
                vol_ccy_quote DECIMAL(30,15),
                confirm VARCHAR(10),
                PRIMARY KEY (ts)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            cursor.execute(sql)
        # 不关闭连接，保持持久化
        print(f"表 {CONFIG['MYSQL_TABLE']} 已准备就绪")
        return True
    except Exception as e:
        print(f"创建表失败: {e}")
        return False


def save_to_mysql(df):
    """将DataFrame数据保存到MySQL表中"""
    connection = create_connection()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            # 准备SQL语句
            sql = f"""
            INSERT INTO {CONFIG['MYSQL_TABLE']} 
            (ts, open, high, low, close, volume, vol_ccy, vol_ccy_quote, confirm)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            open = VALUES(open),
            high = VALUES(high),
            low = VALUES(low),
            close = VALUES(close),
            volume = VALUES(volume),
            vol_ccy = VALUES(vol_ccy),
            vol_ccy_quote = VALUES(vol_ccy_quote),
            confirm = VALUES(confirm)
            """

            # 准备数据
            data = []
            for _, row in df.iterrows():
                data.append((
                    row['ts'],
                    row['open'],
                    row['high'],
                    row['low'],
                    row['close'],
                    row['volume'],
                    row['vol_ccy'],
                    row['vol_ccy_quote'],
                    row['confirm']
                ))

            # 批量插入数据
            cursor.executemany(sql, data)
        # 提交事务，但不关闭连接
        connection.commit()
        print(f"已成功将 {len(df)} 条数据写入MySQL表 {CONFIG['MYSQL_TABLE']}")
        return True
    except Exception as e:
        print(f"写入MySQL失败: {e}")
        connection.rollback()  # 出错时回滚事务
        return False


# ======================
# 初始化API客户端
# ======================
market_data_api = MarketData.MarketAPI(flag=CONFIG["API_ENV"], proxy='http://127.0.0.1:7890')


# ======================
# 加载保存的状态
# ======================
def load_state():
    state_path = CONFIG["SAVE_PATH"] + CONFIG["STATE_FILE"]
    if os.path.exists(state_path):
        try:
            with open(state_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载状态文件失败: {e}，将重新开始下载")
    return None


# ======================
# 保存当前状态
# ======================
def save_state(state):
    state_path = CONFIG["SAVE_PATH"] + CONFIG["STATE_FILE"]
    try:
        with open(state_path, 'w') as f:
            json.dump(state, f)
    except Exception as e:
        print(f"保存状态文件失败: {e}")


# ======================
# 带重试机制的API请求
# ======================
def fetch_data_with_retry(after_ts):
    retries = 0
    while retries < CONFIG["MAX_RETRIES"]:
        try:
            # 发起API请求
            response = market_data_api.get_history_candlesticks(
                instId=CONFIG["INST_ID"],
                after=str(after_ts),
                bar=CONFIG["BAR"],
                limit=str(CONFIG["LIMIT"])
            )

            # 检查API响应状态
            if response["code"] != "0":
                error_msg = f"API请求失败 (Code: {response['code']}): {response['msg']}"

                # 特殊处理超时错误
                if response["code"] == "51054":
                    print(f"请求超时，尝试重试 ({retries + 1}/{CONFIG['MAX_RETRIES']})...")
                    retries += 1
                    # 指数退避策略
                    delay = CONFIG["RETRY_DELAY"] * (2 ** retries) + random.uniform(0, CONFIG["RANDOM_DELAY"])
                    print(f"等待 {delay:.2f} 秒后重试...")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(error_msg)

            return response

        except Exception as e:
            print(f"API请求异常: {str(e)}")
            retries += 1
            if retries < CONFIG["MAX_RETRIES"]:
                delay = CONFIG["RETRY_DELAY"] * (2 ** retries) + random.uniform(0, CONFIG["RANDOM_DELAY"])
                print(f"等待 {delay:.2f} 秒后重试 ({retries}/{CONFIG['MAX_RETRIES']})...")
                time.sleep(delay)
            else:
                raise Exception("达到最大重试次数，下载中断")


# ======================
# 数据获取主程序
# ======================
def main():
    global connection
    try:
        # 创建保存目录
        os.makedirs(CONFIG["SAVE_PATH"], exist_ok=True)

        # 确保MySQL表存在
        if not create_table_if_not_exists():
            print("无法创建MySQL表，程序退出")
            return

        # 加载之前的下载状态
        state = load_state()

        if state:
            print("检测到之前的下载进度，继续下载...")
            current_after_ts = state["current_after_ts"]
            total_records = state["total_records"]
            last_saved_time = datetime.datetime.fromtimestamp(state["last_saved_time"] / 1000)
            print(f"上次保存时间: {last_saved_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"已下载记录数: {total_records}")
        else:
            # 计算新的时间范围
            end_time = datetime.datetime.now()
            start_time = end_time - datetime.timedelta(days=CONFIG["TIME_RANGE_DAYS"])
            current_after_ts = int(end_time.timestamp() * 1000)
            total_records = 0

            print(f"开始全新下载 {CONFIG['INST_ID']} 的 {CONFIG['BAR']} K线数据 (近{CONFIG['TIME_RANGE_DAYS']}天)")
            print(
                f"目标时间范围: {start_time.strftime('%Y-%m-%d %H:%M:%S')} 至 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 数据获取参数
        request_count = 0
        start_time_window = time.time()
        batch_data = []

        # 数据获取主循环
        while True:
            try:
                # 处理API限速 (20次/2秒)
                request_count += 1
                if request_count > 20:
                    elapsed = time.time() - start_time_window
                    if elapsed < 2:
                        time.sleep(2 - elapsed)
                    request_count = 0
                    start_time_window = time.time()

                # 发起API请求（带重试机制）
                response = fetch_data_with_retry(current_after_ts)

                page_data = response.get("data", [])
                if not page_data:
                    print("API返回空数据，可能已无更多历史数据")
                    break

                # 解析数据并添加到批次 (反转顺序，使其按时间正序排列)
                page_data_sorted = sorted(page_data, key=lambda x: int(x[0]))  # 按时间戳升序排列
                batch_data.extend(page_data_sorted)
                total_records += len(page_data)

                # 获取当前页最早的时间戳 (用于下一页请求)
                oldest_ts_in_page = int(page_data[-1][0])  # 原始数据按时间倒序排列，最后一个是最早的

                # 打印进度
                oldest_time = datetime.datetime.fromtimestamp(oldest_ts_in_page // 1000)
                print(
                    f"已获取 {len(page_data)} 条数据 | 最早数据时间: {oldest_time.strftime('%Y-%m-%d %H:%M:%S')} | 累计数据: {total_records}")

                # 判断是否达到时间范围边界
                start_ts = int(
                    (datetime.datetime.now() - datetime.timedelta(days=CONFIG["TIME_RANGE_DAYS"])).timestamp() * 1000)
                if oldest_ts_in_page <= start_ts:
                    print("已到达目标时间范围的起始时间")
                    break

                # 更新下一页的after参数 (减1毫秒避免重复获取)
                current_after_ts = oldest_ts_in_page - 1

                # 达到最大数据量限制
                if total_records >= CONFIG["MAX_DATA_LIMIT"]:
                    print(f"警告：已达到最大数据量限制 ({CONFIG['MAX_DATA_LIMIT']} 条)")
                    break

                # 每获取1000条数据保存一次
                if len(batch_data) >= 1000:
                    # 数据处理与保存
                    df = pd.DataFrame(
                        batch_data,
                        columns=["ts", "open", "high", "low", "close", "volume", "vol_ccy", "vol_ccy_quote", "confirm"]
                    )
                    df["ts"] = pd.to_datetime(df["ts"].astype(int), unit="ms")  # 转换时间戳为datetime

                    # 确保数据按时间正序排列
                    df = df.sort_values("ts").reset_index(drop=True)

                    # 保存到MySQL表
                    if save_to_mysql(df):
                        print(f"已成功保存 {len(batch_data)} 条数据到MySQL表")

                        # 保存当前状态
                        state = {
                            "current_after_ts": current_after_ts,
                            "total_records": total_records,
                            "last_saved_time": current_after_ts
                        }
                        save_state(state)

                        # 清空批次数据
                        batch_data = []
                    else:
                        print("保存数据到MySQL失败，程序退出")
                        return

                # 安全间隔 (避免突发流量)
                time.sleep(0.1)

            except Exception as e:
                print(f"发生异常: {str(e)}")
                print("保存当前状态并退出...")

                # 保存当前状态
                state = {
                    "current_after_ts": current_after_ts,
                    "total_records": total_records,
                    "last_saved_time": current_after_ts
                }
                save_state(state)

                # 保存剩余批次数据
                if batch_data:
                    df = pd.DataFrame(
                        batch_data,
                        columns=["ts", "open", "high", "low", "close", "volume", "vol_ccy", "vol_ccy_quote", "confirm"]
                    )
                    df["ts"] = pd.to_datetime(df["ts"].astype(int), unit="ms")
                    df = df.sort_values("ts").reset_index(drop=True)

                    if save_to_mysql(df):
                        print(f"已成功保存剩余 {len(batch_data)} 条数据到MySQL表")
                    else:
                        print("保存剩余数据到MySQL失败")

                print("程序已暂停。可随时重新运行以继续下载。")
                return

        # 处理剩余数据
        if batch_data:
            df = pd.DataFrame(
                batch_data,
                columns=["ts", "open", "high", "low", "close", "volume", "vol_ccy", "vol_ccy_quote", "confirm"]
            )
            df["ts"] = pd.to_datetime(df["ts"].astype(int), unit="ms")

            # 确保数据按时间正序排列
            df = df.sort_values("ts").reset_index(drop=True)

            if save_to_mysql(df):
                print(f"已成功保存剩余 {len(batch_data)} 条数据到MySQL表")

                # 删除状态文件，表示下载完成
                state_path = CONFIG["SAVE_PATH"] + CONFIG["STATE_FILE"]
                if os.path.exists(state_path):
                    os.remove(state_path)
                    print("已删除状态文件")

                print(f"\n数据已完整保存到MySQL表: {CONFIG['MYSQL_TABLE']}")
                print(f"总行数: {total_records}")
            else:
                print("保存剩余数据到MySQL失败")
        else:
            print("没有需要保存的剩余数据")
            print(f"\n数据已完整保存到MySQL表: {CONFIG['MYSQL_TABLE']}")
            print(f"总行数: {total_records}")

    finally:
        # 程序结束时关闭数据库连接
        if connection and connection.open:
            connection.close()
            print("已关闭数据库连接")


if __name__ == "__main__":
    main()
