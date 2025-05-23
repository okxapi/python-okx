import csv
import time
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from okx.Trade import TradeAPI
from okx import MarketData, PublicData

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

# 缓存产品信息，避免重复查询
instrument_cache = {}


def get_instrument_info(inst_id: str) -> Optional[Dict]:
    """获取产品基础信息，包括最小下单量等参数"""
    global instrument_cache

    # 优先使用缓存
    if inst_id in instrument_cache:
        return instrument_cache[inst_id]

    try:
        # 根据instId推断instType
        if "-SWAP" in inst_id:
            inst_type = "SWAP"
        elif "-FUTURES" in inst_id:
            inst_type = "FUTURES"
        elif "-OPTION" in inst_id:
            inst_type = "OPTION"
        elif "-MARGIN" in inst_id:
            inst_type = "MARGIN"
        else:
            inst_type = "SPOT"

        # 查询产品信息
        result = public_api.get_instruments(instType=inst_type, instId=inst_id)
        if result["code"] == "0" and len(result["data"]) > 0:
            info = result["data"][0]
            instrument_cache[inst_id] = info
            return info
        else:
            print(f"获取{inst_id}产品信息失败: {result.get('msg', '无错误信息')}")
            return None
    except Exception as e:
        print(f"查询产品信息异常: {str(e)}")
        return None


from functools import lru_cache
from datetime import datetime, timedelta


def get_realtime_price(inst_id: str) -> Dict[str, float]:
    """获取实时行情数据(带2分钟缓存)"""

    @lru_cache(maxsize=128)
    def _get_cached_price(inst_id: str, timestamp: str) -> Dict[str, float]:
        """内部缓存函数，通过时间戳控制缓存有效期"""
        try:
            result = market_api.get_ticker(instId=inst_id)
            if result["code"] == "0" and len(result["data"]) > 0:
                data = result["data"][0]
                return {
                    "ask_px": float(data["askPx"]),
                    "bid_px": float(data["bidPx"])
                }
            else:
                print(f"行情查询失败: {result.get('msg', '无错误信息')}")
                return {}
        except Exception as e:
            print(f"行情接口异常: {str(e)}")
            return {}

    # 生成2分钟精度的时间戳作为缓存key
    current_time = datetime.now()
    # 计算当前时间向下取整到最近的2分钟
    timestamp = current_time - timedelta(minutes=current_time.minute % 2,
                                         seconds=current_time.second,
                                         microseconds=current_time.microsecond)
    # 将时间戳转为字符串作为缓存标识
    timestamp_str = timestamp.strftime("%Y%m%d%H%M")

    return _get_cached_price(inst_id, timestamp_str)


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

            # 获取产品信息
            instrument_info = get_instrument_info(uly)
            if not instrument_info:
                print(f"跳过{row['ordId']}: 无法获取产品信息")
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
                adjusted_px = min(original_px, price_data["ask_px"])
            elif side == "sell":
                adjusted_px = max(original_px, price_data["bid_px"])
            else:
                print(f"未知方向{side}，使用原始价格")
                adjusted_px = original_px

            # 计算下单数量
            base_sz = value_amount / original_px
            adjusted_sz = base_sz * 0.035

            # 数量精度处理
            min_sz = float(instrument_info["minSz"])
            lot_sz = float(instrument_info["lotSz"])

            # 确保数量符合最小下单量要求
            if adjusted_sz < min_sz:
                print(f"订单{row['ordId']}数量{adjusted_sz}低于最小下单量{min_sz}，调整为最小下单量")
                adjusted_sz = min_sz

            # 按精度舍入
            def round_to_step(value: float, step: float) -> float:
                """按指定步长舍入"""
                return round(value / step) * step

            final_sz = round_to_step(adjusted_sz, lot_sz)

            # 再次检查是否满足最小下单量
            if final_sz < min_sz:
                final_sz = min_sz
                print(f"订单{row['ordId']}舍入后数量{final_sz}仍低于最小下单量")

            # 构造交易参数
            trade_params = {
                "instId": uly,
                "tdMode": "isolated",
                "side": side,
                "ccy": "USDT",
                "ordType": "limit",
                "sz": f"{final_sz:.8f}",  # 数量精度
                "px": f"{adjusted_px:.8f}"  # 价格精度
            }

            # 执行下单
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"[{attempt + 1}/{max_retries}] 提交订单: {trade_params}")
                    result = trade_api.place_order(**trade_params)
                    if result["code"] == "0":
                        print(f"订单{row['ordId']}成功: {result['data']}")
                        row["alias"] = "none"
                        break
                    else:
                        error = result["data"][0]
                        print(f"订单失败: {error['sMsg']}")

                        # 处理特定错误
                        if error["sCode"] == "51137" and "buy orders" in error["sMsg"]:
                            new_px = float(error["sMsg"].split("is ")[1].split(". ")[0])
                            print(f"触发价格限制，使用强制限价: {new_px}")
                            trade_params["px"] = f"{new_px:.8f}"
                        else:
                            row["alias"] = "none"
                            break
                except Exception as e:
                    print(f"下单异常: {str(e)}")
                    if attempt == max_retries - 1:
                        row["alias"] = "none"
            time.sleep(1)  # API调用间隔
            writer.writerow(row)

    os.replace(temp_file, file_path)
    print(f"处理完成，更新文件: {file_path}")

# while True:
#     try:
#     # 执行处理
#         process_trade_records()
#     except:
#         continue
#     time.sleep(5)