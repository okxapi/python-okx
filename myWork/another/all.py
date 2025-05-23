import csv
import time
from typing import List, Dict
import os
from dotenv import load_dotenv  # 导入 dotenv 库

# 加载 .env 文件中的环境变量
load_dotenv()

from okx.Trade import TradeAPI

# 初始化API客户端

api_key = os.getenv("OKX_API_KEY")
api_secret_key = os.getenv("OKX_API_SECRET")
passphrase = os.getenv("OKX_API_PASSPHRASE")
ENV_FLAG = os.getenv("OKX_ENV_FLAG")
trade_api = TradeAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='0')


def process_trade_records(file_path: str = "trade_records.csv") -> None:
    """
    处理交易记录文件，根据uly字段动态设置交易对，从avgPx读取价格，
    并根据value和avgPx计算交易数量（添加0.035的系数调整）
    """
    temp_file = "temp_trade_records.csv"

    with open(file_path, "r", encoding="utf-8") as infile, \
            open(temp_file, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()

        for row in reader:
            alias = row.get("alias", "").strip().lower()
            uly = row.get("uly", "")
            side = row.get("side", "")
            avg_px = row.get("avgPx", "")
            value = row.get("value", "")

            # 跳过无效记录
            if alias in ["none", ""]:
                writer.writerow(row)
                continue

            if not uly or not avg_px or not value:
                print(f"跳过无效记录: ordId={row.get('ordId')}, 原因: uly/avgPx/value为空")
                writer.writerow(row)
                continue

            # 数据类型转换与验证
            try:
                px = float(avg_px)
                value_amount = float(value)
                if px <= 0 or value_amount <= 0:
                    raise ValueError("价格或价值必须大于0")
            except (ValueError, TypeError) as e:
                print(f"数据格式错误: {str(e)}")
                writer.writerow(row)
                continue

            # 计算交易数量 (sz = value / px)，并添加系数调整
            base_sz = value_amount / px
            adjustment_coefficient = 0.035  # 调整系数
            adjusted_sz = base_sz * adjustment_coefficient

            # 构造交易参数
            trade_params = {
                "instId": uly,
                "tdMode": "isolated",
                "side": side,
                "ccy":"USDT",
                "ordType": "limit",
                "sz": f"{adjusted_sz:.4f}",  # 保留8位小数
                "px": f"{px:.4f}"  # 保留8位小数
            }

            # 调用交易API
            try:
                print(f"处理订单: ordId={row.get('ordId')},方向={side}, 交易对={uly}, 价格={px}, 数量={adjusted_sz}")
                result = trade_api.place_order(**trade_params)

                if result.get("code") == "0":
                    print(f"订单成功: {result.get('data', '无数据')}")
                    row["alias"] = "none"  # 标记为已处理
                else:
                    print(f"订单失败: {result.get('data', '未知错误')}")
                    row["alias"] = "none"  # 标记为已处理

            except Exception as e:
                print(f"API调用异常: {str(e)}")
                row["alias"] = "none"  # 标记为已处理

            writer.writerow(row)
            time.sleep(0.5)  # 控制API调用频率

    # 替换原始文件
    import os
    os.replace(temp_file, file_path)
    print(f"处理完成，更新后的文件已保存至: {file_path}")


# 执行处理
process_trade_records()
