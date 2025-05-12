import json

from CoinGeckoAPI import CoinGeckoAPI
from myWork.ai.analysis.technical_indicators import calculate_technical_indicators
from ai_analysis import AIAnalyzer
import pandas as pd
from datetime import datetime


def main():
    print("===== BTC 价格预测分析系统 =====")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("--------------------------------\n")

    try:
        # 1. 获取 BTC 价格数据
        print("正在获取 BTC 价格数据...")
        price_data = CoinGeckoAPI.get_btc_price()
        print(f"当前价格: ${price_data['price']:.2f}")
        print(f"24h 变化: {price_data['change_24h']:.2f}%\n")

        # 2. 获取历史数据
        print("正在获取 BTC 历史价格数据...")
        historical_data = CoinGeckoAPI.get_btc_historical_data(days=90)
        historical_df = pd.DataFrame(historical_data)
        print(f"获取了 {len(historical_data)} 天的历史数据\n")

        # 3. 计算技术指标
        print("正在计算技术指标...")
        technical_indicators = calculate_technical_indicators(historical_df)
        print(f"MA5: ${technical_indicators['MA5']:.2f}")
        print(f"MA20: ${technical_indicators['MA20']:.2f}")
        print(f"MA50: ${technical_indicators['MA50']:.2f}")
        print(f"MA200: ${technical_indicators['MA200']:.2f}")
        print(f"RSI: {technical_indicators['RSI']:.2f}")
        print(f"MACD: {technical_indicators['MACD']:.2f}\n")

        # 4. 获取链上数据
        '''
        print("正在获取链上数据...")
        #glassnode_api = GlassnodeAPI()
        # onchain_data = glassnode_api.get_btc_onchain_data()
        print(f"交易所余额: {onchain_data['exchange_balance']:.2f} BTC")
        print(f"24h 交易所净流入: {onchain_data['exchange_flow']:.2f} BTC")
        print(f"巨鲸交易数: {onchain_data['whale_transactions']} 笔")
        print(f"活跃地址数: {onchain_data['active_addresses']:,}\n")

        # 5. 获取恐惧与贪婪指数
        print("正在获取恐惧与贪婪指数...")
        #fear_greed_index = get_fear_greed_index()
        print(f"恐惧与贪婪指数: {fear_greed_index}\n")
        '''

        # 6. 生成 AI 分析
        print("正在生成 AI 分析...")
        analysis_data = {
            "price_data": price_data,
            "technical_indicators": technical_indicators,
            # "onchain_data": onchain_data,
            # "fear_greed_index": fear_greed_index
        }

        analyzer = AIAnalyzer()
        prediction = analyzer.generate_analysis(analysis_data)

        # 7. 打印分析结果
        print("\n===== AI 分析结果 =====")
        print(f"未来 7 天价格区间: {prediction['price_range']}")
        print(f"关键支撑位: {prediction['support_level']}")
        print(f"关键阻力位: {prediction['resistance_level']}")
        print(f"上涨概率: {prediction['bullish_probability']}")
        print(f"下跌概率: {prediction['bearish_probability']}")

        print("\n主要驱动因素:")
        for i, factor in enumerate(prediction['driving_factors'], 1):
            print(f"{i}. {factor}")

        print("\n风险提示:")
        for i, risk in enumerate(prediction['risks'], 1):
            print(f"{i}. {risk}")

        print(f"\n交易建议: {prediction['trading_advice']}")
        print("=======================\n")

        # 8. 保存结果到文件
        with open(f"btc_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(prediction, f, indent=4)
        print("分析结果已保存到文件")

    except Exception as e:
        print(f"分析过程中发生错误: {e}")


if __name__ == "__main__":
    main()
