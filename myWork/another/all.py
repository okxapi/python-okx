import csv
import time
from typing import List, Dict
import os
from dotenv import load_dotenv
from okx.Trade import TradeAPI
from okx import MarketData  # 新增行情查询模块

# 初始化API客户端
load_dotenv()
api_key = os.getenv("OKX_API_KEY")
api_secret_key = os.getenv("OKX_API_SECRET")
passphrase = os.getenv("OKX_API_PASSPHRASE")
ENV_FLAG = os.getenv("OKX_ENV_FLAG")

# 交易API
trade_api = TradeAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag=ENV_FLAG)
# 行情API
market_api = MarketData.MarketAPI(flag=ENV_FLAG)  # 实盘环境，模拟盘请改为1

def get_realtime_price(inst_id: str) -> Dict[str, float]:
    """获取实时行情数据"""
    try:
        result = market_api.get_ticker(instId=inst_id)
        if result["code"] == "0" and len(result["data"]) > 0:
            data = result["data"][0]
            return {
                "ask_px": float(data["askPx"]),  # 卖一价
                "bid_px": float(data["bidPx"])   # 买一价
            }
        else:
            print(f"行情查询失败: {result.get('msg', '无错误信息')}")
            return {}
    except Exception as e:
        print(f"行情接口异常: {str(e)}")
        return {}

def process_trade_records(file_path: str = "trade_records.csv") -> None:
    temp_file = "temp_trade_records.csv"
    with open(file_path, "r", encoding="utf-8") as infile, \
         open(temp_file, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()

        for row in reader:
            alias = row.get("alias", "").strip().lower()
            if alias in ["none", ""]:
                writer.writerow(row)
                continue

            uly = row["uly"]
            side = row["side"].lower()
            try:
                original_px = float(row["avgPx"])
                value_amount = float(row["value"])
            except (ValueError, TypeError):
                print(f"订单{row['ordId']}数据格式错误")
                writer.writerow(row)
                continue

            # 获取实时行情
            price_data = get_realtime_price(uly)
            if not price_data:
                print(f"跳过{row['ordId']}: 行情数据获取失败")
                writer.writerow(row)
                continue

            # 动态调整价格
            if side == "buy":
                # 买单价格不能超过卖一价
                adjusted_px = min(original_px, price_data["ask_px"])
            elif side == "sell":
                # 卖单价格不能低于买一价
                adjusted_px = max(original_px, price_data["bid_px"])
            else:
                print(f"未知方向{side}，使用原始价格")
                adjusted_px = original_px

            # 价格调整日志
            if adjusted_px != original_px:
                print(f"订单{row['ordId']}价格调整: {original_px} → {adjusted_px}")

            # 计算数量（保留8位小数，OKX通常要求4-8位，具体看交易对）
            base_sz = value_amount / original_px
            adjusted_sz = base_sz * 0.00035
            sz = f"{adjusted_sz:.8f}"
            px = f"{adjusted_px:.8f}"

            # 构造交易参数
            trade_params = {
                "instId": uly,
                "tdMode": "isolated",
                "side": side,
                "ccy": "USDT",
                "ordType": "limit",
                "sz": sz,
                "px": px
            }

            # 执行下单（带重试机制）
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"[{attempt+1}/{max_retries}] 提交订单: {trade_params}")
                    result = trade_api.place_order(**trade_params)
                    if result["code"] == "0":
                        print(f"订单{row['ordId']}成功: {result['data']}")
                        row["alias"] = "none"
                        break
                    else:
                        # 处理特定错误（如价格限制）
                        error = result["data"][0]
                        if error["sCode"] == "51137" and "buy orders" in error["sMsg"]:
                            # 从错误信息中提取最高限价（备用方案）
                            new_px = float(error["sMsg"].split("is ")[1].split(". ")[0])
                            print(f"触发价格限制，使用强制限价: {new_px}")
                            trade_params["px"] = f"{new_px:.8f}"
                        else:
                            print(f"订单失败: {error['sMsg']}")
                            row["alias"] = "none"
                            break
                except Exception as e:
                    print(f"下单异常: {str(e)}")
                    if attempt == max_retries - 1:
                        row["alias"] = "none"
            time.sleep(1)  # 增加间隔避免API限流
            writer.writerow(row)

    os.replace(temp_file, file_path)
    print(f"处理完成，更新文件: {file_path}")

# 执行处理
process_trade_records()