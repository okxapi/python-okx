import pandas as pd
from io import StringIO


def parse_kline_data(data_string):
    """解析CSV格式的K线数据字符串"""
    # 使用pandas解析CSV，自动识别表头
    df = pd.read_csv(data_string)

    # 重命名字段（如果需要）
    if 'ts' not in df.columns:
        raise ValueError("数据中缺少时间戳列 'ts'")

    # 确保数值列类型正确
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'vol_ccy', 'vol_ccy_quote', 'confirm']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 转换时间戳
    df['ts'] = pd.to_datetime(df['ts'])

    # 过滤未确认的K线（confirm=1表示已确认）
    if 'confirm' in df.columns:
        df = df[df['confirm'] == 1].reset_index(drop=True)

    # 重命名为统一字段名
    if 'open' in df.columns:
        df = df.rename(columns={
            'open': 'o', 'high': 'h', 'low': 'l',
            'close': 'c', 'volume': 'vol'
        })

    return df


# 示例：从文件加载数据
def load_kline_from_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return parse_kline_data(data)


def save_optimization_results(results_df, file_path='optimization_results.csv', save_all=True):
    """
    保存参数优化结果到CSV文件

    :param results_df: 优化结果DataFrame
    :param file_path: 保存路径（默认：当前目录下的optimization_results.csv）
    :param save_all: 是否保存所有参数组合（否则仅保存前5名）
    """
    if results_df.empty:
        print("警告: 无有效结果可保存")
        return

    # 选择要保存的列（包含核心指标）
    selected_columns = [
        'short_window', 'long_window', 'buy_ratio', 'sell_ratio',
        'total_return', 'final_portfolio', 'trade_count',
        'max_drawdown', 'win_rate', 'avg_return'  # 新增绩效指标（需在回测结果中包含）
    ]

    # 保存所有结果或仅前5名
    df_to_save = results_df if save_all else results_df.head()

    # 保存为CSV（保留4位小数，添加时间戳表头）
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"data/{timestamp}_{file_path}" if save_all else file_path
    df_to_save[selected_columns].to_csv(
        file_name,
        index=False,
        float_format="%.4f"  # 控制小数精度
    )

    print(f"\n数据已保存到: {file_name}")
    print(f"保存列: {', '.join(selected_columns)}")