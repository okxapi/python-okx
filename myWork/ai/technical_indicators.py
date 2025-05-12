import pandas as pd
import numpy as np


def calculate_technical_indicators(prices_df):
    """计算 BTC 技术指标"""
    # 确保数据按日期排序
    prices_df = prices_df.sort_values('date')

    # 计算移动平均线 (MA)
    prices_df['MA5'] = prices_df['price'].rolling(window=5).mean()
    prices_df['MA20'] = prices_df['price'].rolling(window=20).mean()
    prices_df['MA50'] = prices_df['price'].rolling(window=50).mean()
    prices_df['MA200'] = prices_df['price'].rolling(window=200).mean()

    # 计算相对强弱指数 (RSI)
    delta = prices_df['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    prices_df['RSI'] = 100 - (100 / (1 + rs))

    # 计算 MACD
    prices_df['EMA12'] = prices_df['price'].ewm(span=12, adjust=False).mean()
    prices_df['EMA26'] = prices_df['price'].ewm(span=26, adjust=False).mean()
    prices_df['MACD'] = prices_df['EMA12'] - prices_df['EMA26']
    prices_df['MACD_Signal'] = prices_df['MACD'].ewm(span=9, adjust=False).mean()
    prices_df['MACD_Hist'] = prices_df['MACD'] - prices_df['MACD_Signal']

    # 返回最新指标值
    latest = prices_df.iloc[-1]
    return {
        'MA5': latest['MA5'],
        'MA20': latest['MA20'],
        'MA50': latest['MA50'],
        'MA200': latest['MA200'],
        'RSI': latest['RSI'],
        'MACD': latest['MACD'],
        'MACD_Signal': latest['MACD_Signal'],
        'MACD_Hist': latest['MACD_Hist']
    }