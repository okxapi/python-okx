import csv
import time

import requests

from myWork.another.all import process_trade_records


def get_data(user_name):
    url = "https://www.okx.com/priapi/v5/ecotrade/public/community/user/trade-records"
    import time

    # 获取当前时间戳（毫秒级）
    current_time = int(time.time() * 1000)

    # 计算2天前的时间戳（2天 = 2 * 24 * 60 * 60 * 1000毫秒）
    two_days_ago = current_time - 2 * 24 * 60 * 60 * 1000

    params = {
        "uniqueName": user_name,
        "startModify": str(two_days_ago),  # 开始时间：2天前
        "endModify": str(current_time),  # 结束时间：当前时间
        "limit": "120",
        "t": str(current_time)  # 请求时间戳：当前时间
    }

    with open('header.json', 'r') as file:
        headers_content = file.read()
        # 根据文件内容格式解析 headers（示例为 JSON 格式）
        import json
        headers = json.loads(headers_content)


    response = requests.get(url, params=params, headers=headers)

    # 打印响应内容（根据需求处理）
    print(response.text)
    response_json = response.json()
    return response_json


def save_trade_records_to_csv(new_data, file_path="trade_records.csv"):
    """
    将新交易记录增量写入CSV文件，并根据ordId去重

    参数：
    new_data (list): 新交易记录列表（字典格式，需包含ordId字段）
    file_path (str): CSV文件路径（默认当前目录下的trade_records.csv）
    """
    # 1. 读取现有文件中的ordId（用于去重）
    existing_ord_ids = set()
    new_records = []

    # 尝试读取现有文件（若文件不存在则跳过）
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ord_ids.add(row["ordId"])
    except FileNotFoundError:
        pass  # 文件不存在时首次写入

    # 2. 过滤新数据中的重复记录（根据ordId）
    for record in new_data:
        ord_id = record.get("ordId")
        if ord_id and ord_id not in existing_ord_ids:
            new_records.append(record)
            existing_ord_ids.add(ord_id)  # 标记为已存在，避免后续重复

    # 3. 写入新数据到CSV文件（追加模式）
    if new_records:
        # 获取表头（若文件不存在则根据新数据生成）
        headers = new_records[0].keys() if new_records else []

        # 以追加模式打开文件（若文件不存在则创建）
        with open(file_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)

            # 若文件为空，则写入表头
            if not existing_ord_ids:
                writer.writeheader()

            # 写入去重后的新记录
            writer.writerows(new_records)

        print(f"成功写入 {len(new_records)} 条新记录到 {file_path}")
        process_trade_records()
    else:
        print("无新记录需要写入（已全部去重）")


try:
    with open("user", "r") as f:
        params = [line.strip() for line in f if line.strip()]  # 去除空行
except FileNotFoundError:
    print("错误: user文件未找到!")
    exit(1)

# 遍历参数并定期处理
while True:
    try:
        for param in params:
            a = get_data(param)
            new_data = a.get("data", [])
            save_trade_records_to_csv(new_data)
    except:
        continue
    time.sleep(60)  # 处理完所有参数后等待60秒
