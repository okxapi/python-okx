import os
from datetime import datetime

import openai
import json
from typing import Dict, Any
from config import OPENAI_API_KEY
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取配置
API_KEY = os.getenv("OKX_API_KEY")
API_SECRET = os.getenv("OKX_API_SECRET")
PASSPHRASE = os.getenv("OKX_API_PASSPHRASE")
ENV_FLAG = os.getenv("OKX_ENV_FLAG")


class AIAnalyzer:
    SYSTEM_PROMPT = """
    你是一位精通加密货币市场的量化分析师。请基于以下数据，对 BTC 未来 7 天的价格走势进行全面分析：

    1. 技术面分析：MA5/MA20/MA50/MA200 趋势、RSI 指标、MACD 指标
    2. 链上数据：交易所余额变化、巨鲸活动、活跃地址数
    3. 市场情绪：恐惧与贪婪指数
    4. 宏观经济：美元指数、美联储政策预期

    请提供结构化分析，包括：
    - 未来 7 天价格区间预测（精确到 $100）
    - 关键支撑位和阻力位
    - 上涨/下跌概率（百分比）
    - 主要驱动因素（至少 3 条）
    - 重大风险提示（至少 3 条）
    - 明确的交易建议

    请以 JSON 格式返回结果，包含以下字段：
    "price_range", "support_level", "resistance_level", 
    "bullish_probability", "bearish_probability", 
    "driving_factors", "risks", "trading_advice", "analysis_date"
    """

    @staticmethod
    def generate_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
        """生成 AI 分析结果"""
        # 构建用户提示词
        user_prompt = f"""
        当前 BTC 数据：

        1. 价格数据：
           - 当前价格：${data['price_data']['price']:.2f}
           - 24h 变化：{data['price_data']['change_24h']:.2f}%
           - 市值：${data['price_data']['market_cap']:.0f}
           - 24h 交易量：${data['price_data']['volume_24h']:.0f}

        2. 技术指标：
           - MA5：${data['technical_indicators']['MA5']:.2f}
           - MA20：${data['technical_indicators']['MA20']:.2f}
           - MA50：${data['technical_indicators']['MA50']:.2f}
           - MA200：${data['technical_indicators']['MA200']:.2f}
           - RSI：{data['technical_indicators']['RSI']:.2f}
           - MACD：{data['technical_indicators']['MACD']:.2f}

        3. 链上数据：
           - 交易所余额：{data['onchain_data']['exchange_balance']:.2f} BTC
           - 交易所净流入：{data['onchain_data']['exchange_flow']:.2f} BTC (24h)
           - 巨鲸交易数：{data['onchain_data']['whale_transactions']} 笔
           - 活跃地址数：{data['onchain_data']['active_addresses']:,}

        4. 市场情绪：
           - 恐惧与贪婪指数：{data['fear_greed_index']} ({AIAnalyzer._get_fgi_category(data['fear_greed_index'])})

        请基于以上数据，按照指定格式进行分析。
        """

        # 调用 OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": AIAnalyzer.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # 较低的温度使结果更确定性
                max_tokens=1000
            )

            # 解析 AI 响应
            analysis = json.loads(response.choices[0].message.content)
            analysis["analysis_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return analysis

        except Exception as e:
            print(f"Error generating AI analysis: {e}")
            return {
                "error": str(e),
                "price_range": "无法生成预测",
                "support_level": "无法生成预测",
                "resistance_level": "无法生成预测",
                "bullish_probability": "0%",
                "bearish_probability": "0%",
                "driving_factors": ["AI分析失败", "请检查API密钥", "请检查网络连接"],
                "risks": ["AI分析失败风险", "数据获取失败风险", "模型响应异常风险"],
                "trading_advice": "谨慎操作，等待系统恢复正常",
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    @staticmethod
    def _get_fgi_category(fgi: int) -> str:
        """根据恐惧与贪婪指数返回分类"""
        if fgi < 25:
            return "极度恐惧"
        elif fgi < 50:
            return "恐惧"
        elif fgi < 75:
            return "贪婪"
        else:
            return "极度贪婪"