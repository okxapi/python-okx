import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from myWork.process.read import parse_kline_data


def calculate_rsi(data, period=14):
    """
    计算相对强弱指数（RSI）
    """
    deltas = data.diff()
    up = deltas.clip(lower=0)
    down = -deltas.clip(upper=0)
    avg_gain = up.rolling(window=period).mean()
    avg_loss = down.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def prepare_training_data(file_path: str, lookback: int = 60, forecast: int = 1, split_ratio: float = 0.8) -> tuple:
    """
    完整处理K线数据并准备用于模型训练的序列数据

    参数:
        file_path: 历史K线数据文件路径
        lookback: 用于预测的历史数据长度
        forecast: 预测未来数据点的数量
        split_ratio: 训练集与测试集的划分比例

    返回:
        tuple: 包含以下元素的元组
            - X_train: 训练特征数据，形状为 (样本数, 时间步长, 特征数)
            - X_test: 测试特征数据，形状为 (样本数, 时间步长, 特征数)
            - y_train: 训练目标数据，形状为 (样本数, 预测步长)
            - y_test: 测试目标数据，形状为 (样本数, 预测步长)
            - scaler: 标准化器实例，用于后续数据还原
            - df_processed: 处理后的完整DataFrame
    """
    # 读取并解析数据
    df = parse_kline_data(file_path)

    # 添加技术指标
    df['ma5'] = df['c'].rolling(5).mean()
    df['ma10'] = df['c'].rolling(10).mean()
    df['rsi'] = calculate_rsi(df['c'], 14)

    # 移除包含NaN的行
    df.dropna(inplace=True)

    # 数据标准化
    columns_to_scale = ['o', 'h', 'l', 'c', 'vol', 'ma5', 'ma10', 'rsi']
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

    # 创建序列数据
    X, y = [], []
    for i in range(len(df_scaled) - lookback - forecast + 1):
        X.append(df_scaled.iloc[i:i + lookback][columns_to_scale].values)
        y.append(df_scaled['c'].iloc[i + lookback:i + lookback + forecast].values)
    X, y = np.array(X), np.array(y)

    # 划分训练集和测试集
    split_idx = int(len(X) * split_ratio)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    return X_train, X_test, y_train, y_test, scaler, df_scaled


# 示例调用
if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler, df_processed = prepare_training_data(
        file_path='../sorted_history.csv',
        lookback=60,
        forecast=1,
        split_ratio=0.8
    )

    print("训练集X形状:", X_train.shape)
    print("测试集X形状:", X_test.shape)
    print("训练集y形状:", y_train.shape)
    print("测试集y形状:", y_test.shape)
