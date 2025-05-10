from myWork.process.read import save_optimization_results
from myWork.process.优化参数 import optimize_trading_params
from myWork.process.总流程 import kline_df

def main():
    # 定义待优化的参数范围（可根据经验调整）
    param_ranges = {
        'short_window': range(10, 120, 10),   # 短周期均线：10, 20, 30, 40, 50
        'long_window': range(100, 400, 50),  # 长周期均线：100, 150, 200, 250, 300, 350
        'buy_ratio': [0.2, 0.4,],  # 买入资金比例（1.0为全仓）
        'sell_ratio': [0.2, 0.4]   # 卖出持仓比例（1.0为全仓）
    }

    # 执行参数优化
    optimized_results = optimize_trading_params(
        kline_df=kline_df,
        param_ranges=param_ranges,
        initial_balance=100000,
        fees=(0.001, 0.001),
        max_workers=4
    )

    # 打印前5名最优参数组合
    print("\n==== 最优参数组合（按总收益率排序） ====")
    print(optimized_results[['short_window', 'long_window', 'buy_ratio', 'sell_ratio', 'total_return', 'final_portfolio']].head())

    save_optimization_results(optimized_results, file_path='ma_strategy_optimization.csv')

if __name__ == '__main__':
    main()