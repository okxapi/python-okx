import os
import json
import time
from datetime import datetime
from okx.Trade import TradeAPI
import main

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
        analysis_data =  main.get_ai_predict()


        # 提取交易建议和价格水平
        advice = analysis_data.get("trading_advice", "")
        support_level = analysis_data.get("support_level", "")
        resistance_level = analysis_data.get("resistance_level", "")

        # 提取具体的价格数值（去掉$符号并转为float）
        support_price = float(support_level.replace("$", "").replace(",", ""))
        resistance_price = float(resistance_level.replace("$", "").replace(",", ""))

        return {
            "advice": advice,
            "support_price": support_price,
            "resistance_price": resistance_price
        }
    except Exception as e:
        print(f"解析分析结果出错: {e}")
        return None


def execute_trades(analysis):
    """根据分析结果执行交易"""
    if not analysis:
        print("没有有效的分析结果，无法执行交易")
        return

    advice = analysis["advice"]
    support_price = analysis["support_price"]
    resistance_price = analysis["resistance_price"]

    print(f"分析建议: {advice}")
    print(f"支撑位: {support_price}")
    print(f"阻力位: {resistance_price}")

    # 下单参数
    instId = "BTC-USDT"  # 交易对
    tdMode = "cross"  # 交易模式：逐仓

    # 确定下单方向和价格
    if "逢低布局多单" in advice:
        # 做多策略
        side = "buy"
        # 设置买入价格略高于支撑位
        buy_price = round(support_price * 1.005, 2)  # 比支撑位高0.5%
        order_size = "0.01"  # 下单数量

        print(f"准备执行多单: 价格={buy_price}, 数量={order_size}")

        # 执行买入订单
        result = trade_api.place_order(
            instId=instId,
            tdMode=tdMode,
            side=side,
            ordType="limit",
            sz=order_size,
            px=str(buy_price)
        )

        print(f"多单执行结果: {result}")

        # 设置止损单
        stop_loss_price = round(support_price * 0.99, 2)  # 止损价格比支撑位低1%
        result = trade_api.place_order(
            instId=instId,
            tdMode=tdMode,
            side="sell",  # 止损是卖出
            ordType="stop-loss",
            sz=order_size,
            px=str(stop_loss_price),
            triggerPx=str(stop_loss_price)
        )

        print(f"止损单执行结果: {result}")

    elif "轻仓试空" in advice:
        # 做空策略
        side = "sell"
        # 设置卖出价格略低于阻力位
        sell_price = round(resistance_price * 0.995, 2)  # 比阻力位低0.5%
        order_size = "0.01"  # 下单数量

        print(f"准备执行空单: 价格={sell_price}, 数量={order_size}")

        # 执行卖出订单
        result = trade_api.place_order(
            instId=instId,
            tdMode=tdMode,
            side=side,
            ordType="limit",
            sz=order_size,
            px=str(sell_price)
        )

        print(f"空单执行结果: {result}")

        # 设置止损单
        stop_loss_price = round(resistance_price * 1.01, 2)  # 止损价格比阻力位高1%
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
    else:
        print("未识别到明确的交易建议，暂不执行交易")


def mian():
    """主函数：获取分析结果并执行交易"""
    print(f"开始执行交易策略: {datetime.now()}")


    # 解析分析结果
    analysis = parse_analysis_result()

    # 执行交易
    execute_trades(analysis)

    print(f"交易策略执行完成: {datetime.now()}")

while True:
    try:
        mian()
    except:
        time.sleep(1)
    time.sleep(150)