import os
import json
import time
from datetime import datetime
from okx.Trade import TradeAPI
import precheck
from myWork.ai.CoinGeckoAPI import CoinGeckoAPI

# 获取API凭证
api_key = os.getenv("OKX_API_KEY")
api_secret_key = os.getenv("OKX_API_SECRET")
passphrase = os.getenv("OKX_API_PASSPHRASE")
ENV_FLAG = os.getenv("OKX_ENV_FLAG")

# 初始化交易API
trade_api = TradeAPI(api_key, api_secret_key, passphrase, use_server_time=False, flag='1')


def parse_analysis_result():
    """解析AI分析结果，提取交易建议"""
    try:
        # 提取message中的内容

        # 解析JSON
        analysis_data =  precheck.get_ai_predict()

        # 提取交易建议和关键价格水平
        prediction = {
            "price_range": analysis_data.get("price_range", "未提供"),
            "support_level": analysis_data.get("support_level", "未提供"),
            "resistance_level": analysis_data.get("resistance_level", "未提供"),
            "bullish_probability": f"{analysis_data.get('bullish_probability', 0)}%",
            "bearish_probability": f"{analysis_data.get('bearish_probability', 0)}%",
            "driving_factors": analysis_data.get("driving_factors", []),
            "risks": analysis_data.get("risks", []),
            "trading_advice": analysis_data.get("trading_advice", "未提供")
        }
        return prediction
    except Exception as e:
        print(f"解析分析结果出错: {e}")
        return None


def extract_price_from_text(text, keyword, delimiter):
    """从文本中提取价格信息"""
    if keyword in text:
        start_idx = text.find(keyword) + len(keyword)
        price_text = text[start_idx:]
        if delimiter:
            end_idx = price_text.find(delimiter)
            if end_idx != -1:
                price_text = price_text[:end_idx]
        # 清理价格文本并转换为float
        price_text = price_text.replace("$", "").replace(",", "").strip()
        try:
            return float(price_text)
        except ValueError:
            print(f"无法将价格文本转换为数字: {price_text}")
    return None


def execute_trades(analysis):
    """根据分析结果执行交易"""
    if not analysis:
        print("没有有效的分析结果，无法执行交易")
        return

    advice = analysis["trading_advice"]
    entry_price = advice["entry_point"]
    stop_loss_price = advice["stop_loss"]
    add_position_price = analysis["resistance_level"]
    target_price = advice["target_profit"]

    print(f"分析建议: {advice}")
    print(f"入场价格: {entry_price}")
    print(f"止损价格: {stop_loss_price}")
    print(f"追加仓位价格: {add_position_price}")
    print(f"目标价格: {target_price}")

    # 下单参数
    instId = "BTC-USDT"  # 交易对
    tdMode = "cross"  # 交易模式：逐仓

    # 检查当前市场价格（这里需要调用API获取，示例中使用模拟值）
    current_price = get_current_price(instId)
    print(f"当前市场价格: {current_price}")

    # 确定下单方向和价格
    if "空" in advice and entry_price:
        # 初始空单策略
        side = "sell"
        order_size = "0.01"  # 基础仓位

        # 计算实际下单价格（略低于建议入场价）
        actual_entry_price = round(entry_price * 0.999, 2)

        print(f"准备执行初始空单: 价格={actual_entry_price}, 数量={order_size}")

        # 执行卖出订单
        result = trade_api.place_order(
            instId=instId,
            tdMode=tdMode,
            side=side,
            ordType="limit",
            sz=order_size,
            px=str(actual_entry_price)
        )

        print(f"初始空单执行结果: {result}")

        # 设置止损单
        if stop_loss_price:
            stop_loss_price = round(stop_loss_price, 2)  # 确保止损价格精度
            result = trade_api.place_order(
                instId=instId,
                tdMode=tdMode,
                side="buy",  # 止损是买入
                ordType="stop-loss",
                sz=order_size,
                px=str(stop_loss_price),
                triggerPx=str(stop_loss_price)
            )
            print(f"止损单执行结果: {result}")

        # 设置目标价止盈单
        if target_price:
            take_profit_price = round(target_price, 2)  # 确保目标价格精度
            result = trade_api.place_order(
                instId=instId,
                tdMode=tdMode,
                side="buy",  # 止盈是买入
                ordType="take-profit",
                sz=order_size,
                px=str(take_profit_price),
                triggerPx=str(take_profit_price)
            )
            print(f"止盈单执行结果: {result}")

    # 检查是否需要追加空头仓位
    if "追加" in advice and add_position_price and current_price < add_position_price:
        side = "sell"
        add_size = "0.005"  # 追加仓位大小（可以根据需要调整）

        # 计算追加仓位的下单价格（略低于当前价格）
        add_price = round(current_price * 0.999, 2)

        print(f"价格已跌破{add_position_price}，准备追加空头仓位: 价格={add_price}, 数量={add_size}")

        # 执行追加仓位订单
        result = trade_api.place_order(
            instId=instId,
            tdMode=tdMode,
            side=side,
            ordType="limit",
            sz=add_size,
            px=str(add_price)
        )

        print(f"追加空单执行结果: {result}")

        # 更新止损单（可选，根据策略调整）
        if stop_loss_price:
            # 先撤销原止损单（需要实现cancel_order函数）
            # cancel_order(instId, "stop-loss", "buy")

            # 设置新的移动止损单
            new_stop_loss = round((entry_price + current_price) / 2, 2)  # 移动止损到入场价和当前价的中间
            result = trade_api.place_order(
                instId=instId,
                tdMode=tdMode,
                side="buy",
                ordType="stop-loss",
                sz=str(float(order_size) + float(add_size)),  # 总仓位
                px=str(new_stop_loss),
                triggerPx=str(new_stop_loss)
            )
            print(f"移动止损单执行结果: {result}")
    else:
        print("未满足追加空头仓位的条件")


def get_ai_predict():
    """获取AI预测结果（需要根据实际情况实现）"""
    # 这里应该调用实际的AI预测API
    # 示例返回一个模拟结果
    return {
        "trading_advice": "建议在$103500附近布局空单，止损$104500上方；若价格跌破$99500可追加空头仓位，短期目标价$97000"
    }


def get_current_price(instId):
    """获取当前市场价格（需要根据实际情况实现）"""
    # 这里应该调用OKX的市场数据API
    # 示例返回一个模拟价格
    return CoinGeckoAPI.get_btc_price()


def cancel_order(instId, ordType, side):
    """撤销指定类型的订单（需要根据实际情况实现）"""
    # 实际实现中需要调用OKX的撤销订单API
    print(f"撤销订单: {instId}, {ordType}, {side}")
    return {"code": 0, "msg": "success"}


def main():
    """主函数：获取分析结果并执行交易"""
    print(f"开始执行交易策略: {datetime.now()}")

    try:
        # 解析分析结果
        analysis = parse_analysis_result()

        # 执行交易
        execute_trades(analysis)

        print(f"交易策略执行完成: {datetime.now()}")
    except Exception as e:
        print(f"执行交易策略出错: {e}")


if __name__ == "__main__":
    '''
    while True:
        main()
        time.sleep(150)  # 每2.5分钟执行一次策略
    '''
    filename = "result/btc_prediction_20250513_021802.json"

    # 读取文件
    with open(filename, "r", encoding="utf-8") as f:
        prediction = json.load(f)
    execute_trades(prediction)