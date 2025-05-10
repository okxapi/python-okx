import okx.MarketData as MarketData
import time
import datetime
import pandas as pd
import os
import json
import random
from tqdm import tqdm

# ======================
# 配置参数
# ======================
CONFIG = {
    "API_ENV": "0",  # 0: 实盘, 1: 模拟盘
    "INST_ID": "BTC-USDT",  # 交易对
    "BAR": "1m",  # 时间粒度 (1s/1m/3m/5m/15m/30m/1H/2H/4H/6H/12H/1D等)
    "LIMIT": 100,  # 每页数据量 (最大100)
    "TIME_RANGE_DAYS": 365,  # 时间范围 (天数)
    "MAX_DATA_LIMIT": 10000000,  # 最大数据量限制
    "SAVE_PATH": "./",  # 数据保存路径 (结尾带/)
    "TEMP_FILE": "temp_history.csv",  # 临时数据文件名
    "FINAL_FILE": "sorted_history.csv",  # 最终排序后文件名
    "STATE_FILE": "download_state.json",  # 状态保存文件名
    "MAX_RETRIES": 5,  # API请求最大重试次数
    "RETRY_DELAY": 5,  # 重试前等待秒数 (基础值)
    "RANDOM_DELAY": 3  # 随机延迟上限 (避免请求风暴)
}

# ======================
# 初始化API客户端
# ======================
market_data_api = MarketData.MarketAPI(flag=CONFIG["API_ENV"])


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
# 按时间对整个CSV文件进行排序
# ======================
def sort_csv_by_time():
    temp_file = CONFIG["SAVE_PATH"] + CONFIG["TEMP_FILE"]
    final_file = CONFIG["SAVE_PATH"] + CONFIG["FINAL_FILE"]

    if not os.path.exists(temp_file):
        print("错误：找不到临时数据文件")
        return

    print("开始对数据进行最终排序...")

    # 读取并排序整个文件
    try:
        # 分块读取大型CSV文件
        chunksize = 100000
        chunks = []

        # 显示读取进度
        file_size = os.path.getsize(temp_file)
        progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc="读取数据")

        bytes_read = 0
        for chunk in pd.read_csv(temp_file, chunksize=chunksize):
            # 将时间戳转换为datetime类型
            chunk['ts'] = pd.to_datetime(chunk['ts'])
            # 对每个块进行排序
            chunk = chunk.sort_values('ts')
            chunks.append(chunk)
            bytes_read += chunk.memory_usage(deep=True).sum()
            progress_bar.update(bytes_read - progress_bar.n)

        progress_bar.close()

        # 合并所有块
        print("合并并写入排序后的数据...")
        all_data = pd.concat(chunks, ignore_index=True)
        del chunks  # 释放内存

        # 写入到新文件
        all_data.to_csv(final_file, index=False)

        print(f"排序完成！最终文件保存在: {final_file}")
        print(f"总行数: {len(all_data)}")
        print(f"时间范围: {all_data['ts'].min()} 至 {all_data['ts'].max()}")

        # 可选：删除临时文件
        print("正在删除临时文件...")
        os.remove(temp_file)
        print("临时文件已删除")

    except Exception as e:
        print(f"排序过程中发生错误: {e}")
        print(f"部分数据可能已保存到 {final_file}，但可能不完整")


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
    # 创建保存目录
    os.makedirs(CONFIG["SAVE_PATH"], exist_ok=True)

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
        print(f"目标时间范围: {start_time.strftime('%Y-%m-%d %H:%M:%S')} 至 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

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

                # 保存为CSV文件
                file_path = f"{CONFIG['SAVE_PATH']}{CONFIG['TEMP_FILE']}"
                file_exists = os.path.exists(file_path)

                try:
                    df.to_csv(file_path, mode='a', index=False, header=not file_exists)
                    print(f"已追加保存 {len(batch_data)} 条数据到文件")

                    # 保存当前状态
                    state = {
                        "current_after_ts": current_after_ts,
                        "total_records": total_records,
                        "last_saved_time": current_after_ts
                    }
                    save_state(state)

                    # 清空批次数据
                    batch_data = []

                except Exception as e:
                    print(f"保存文件失败: {str(e)}")
                    print("请检查保存路径是否存在，或是否有写入权限")
                    break

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

                file_path = f"{CONFIG['SAVE_PATH']}{CONFIG['TEMP_FILE']}"
                file_exists = os.path.exists(file_path)

                try:
                    df.to_csv(file_path, mode='a', index=False, header=not file_exists)
                    print(f"已保存剩余 {len(batch_data)} 条数据")
                except Exception as save_e:
                    print(f"保存剩余数据失败: {str(save_e)}")

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

        file_path = f"{CONFIG['SAVE_PATH']}{CONFIG['TEMP_FILE']}"
        file_exists = os.path.exists(file_path)

        try:
            df.to_csv(file_path, mode='a', index=False, header=not file_exists)
            print(f"已追加保存剩余 {len(batch_data)} 条数据到文件")

            # 删除状态文件，表示下载完成
            state_path = CONFIG["SAVE_PATH"] + CONFIG["STATE_FILE"]
            if os.path.exists(state_path):
                os.remove(state_path)
                print("已删除状态文件")

            print(f"\n临时数据已完整保存到文件: {file_path}")

            # 执行最终排序
            sort_csv_by_time()

        except Exception as e:
            print(f"保存剩余数据失败: {str(e)}")
            print("下载未完成，请重新运行程序继续下载")
    else:
        print("没有需要保存的剩余数据")
        # 如果没有剩余数据但已下载过部分数据，也执行排序
        if os.path.exists(CONFIG["SAVE_PATH"] + CONFIG["TEMP_FILE"]):
            sort_csv_by_time()


if __name__ == "__main__":
    main()