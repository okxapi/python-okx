import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pymysql
from sqlalchemy import create_engine, text
import random
from itertools import product
import uuid
import json
from multiprocessing import Pool
from functools import partial
from tqdm import tqdm
from myWork.dca.mysql_read import MySQLDataReader
from myWork.dca.save import run_strategy
from myWork.dca.stg import DCAStrategy


class ParameterTrainingSystem:
    def __init__(self, db_config):
        """初始化参数训练系统，创建必要的数据库表"""
        self.db_config = db_config
        self.engine = create_engine(
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        self._create_tables()

    def _create_tables(self):
        """创建存储参数和结果的数据库表"""
        with self.engine.connect() as conn:
            # 创建参数配置表 - 添加了currency列
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dca_parameter_configs (
                config_id VARCHAR(36) PRIMARY KEY,
                config_name VARCHAR(255) NOT NULL,
                currency VARCHAR(50) NOT NULL,  # 新增：币种
                base_config TEXT NOT NULL,
                param_ranges TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                status ENUM('pending', 'running', 'completed', 'failed') NOT NULL DEFAULT 'pending'
            )
            """))

            # 创建参数组合表 - 添加了currency列
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dca_parameter_combinations (
                combination_id VARCHAR(36) PRIMARY KEY,
                config_id VARCHAR(36) NOT NULL,
                currency VARCHAR(50) NOT NULL,  # 新增：币种
                parameters TEXT NOT NULL,
                result TEXT,
                status ENUM('pending', 'running', 'completed', 'failed') NOT NULL DEFAULT 'pending',
                worker_id VARCHAR(255),
                started_at DATETIME,
                completed_at DATETIME,
                FOREIGN KEY (config_id) REFERENCES dca_parameter_configs(config_id)
            )
            """))

    def save_parameters_for_training(self, config_name, currency, base_config, param_ranges):
        """
        保存参数配置和所有参数组合到数据库

        参数:
        config_name - 配置名称
        currency - 币种
        base_config - 基础策略配置
        param_ranges - 要测试的参数范围字典

        返回:
        config_id - 配置ID
        """
        config_id = str(uuid.uuid4())
        created_at = datetime.now()

        # 保存配置信息
        with self.engine.connect() as conn:
            conn.execute(
                text("""
                INSERT INTO dca_parameter_configs 
                (config_id, config_name, currency, base_config, param_ranges, created_at, status)
                VALUES (:config_id, :config_name, :currency, :base_config, :param_ranges, :created_at, 'pending')
                """),
                {
                    'config_id': config_id,
                    'config_name': config_name,
                    'currency': currency,
                    'base_config': json.dumps(base_config),
                    'param_ranges': json.dumps(param_ranges),
                    'created_at': created_at
                }
            )

            # 生成所有参数组合并保存
            param_names = list(param_ranges.keys())
            param_values = list(param_ranges.values())
            param_combinations = list(product(*param_values))

            for params in param_combinations:
                combination_id = str(uuid.uuid4())
                parameters = {name: value for name, value in zip(param_names, params)}

                conn.execute(
                    text("""
                    INSERT INTO dca_parameter_combinations 
                    (combination_id, config_id, currency, parameters, status)
                    VALUES (:combination_id, :config_id, :currency, :parameters, 'pending')
                    """),
                    {
                        'combination_id': combination_id,
                        'config_id': config_id,
                        'currency': currency,
                        'parameters': json.dumps(parameters)
                    }
                )

        return config_id

    def get_pending_tasks(self, limit=10, currency=None):
        """获取待处理的参数组合任务，可按币种筛选"""
        query = """
        SELECT combination_id, config_id, currency, parameters 
        FROM dca_parameter_combinations 
        WHERE status = 'pending' 
        """
        params = {'limit': limit}

        if currency:
            query += " AND currency = :currency "

        query += " LIMIT :limit"

        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            return [
                {
                    'combination_id': row[0],
                    'config_id': row[1],
                    'currency': row[2],
                    'parameters': json.loads(row[3])
                }
                for row in result.fetchall()
            ]

    def mark_task_status(self, combination_id, status, result=None, worker_id=None):
        """标记任务状态"""
        with self.engine.connect() as conn:
            if status == 'running':
                conn.execute(
                    text("""
                    UPDATE dca_parameter_combinations 
                    SET status = :status, worker_id = :worker_id, started_at = NOW() 
                    WHERE combination_id = :combination_id
                    """),
                    {
                        'combination_id': combination_id,
                        'status': status,
                        'worker_id': worker_id
                    }
                )
            elif status in ['completed', 'failed']:
                conn.execute(
                    text("""
                    UPDATE dca_parameter_combinations 
                    SET status = :status, result = :result, completed_at = NOW() 
                    WHERE combination_id = :combination_id
                    """),
                    {
                        'combination_id': combination_id,
                        'status': status,
                        'result': json.dumps(result) if result else None
                    }
                )

    def get_config_details(self, config_id):
        """获取配置详情"""
        with self.engine.connect() as conn:
            result = conn.execute(
                text("""
                SELECT currency, base_config, param_ranges 
                FROM dca_parameter_configs 
                WHERE config_id = :config_id
                """),
                {'config_id': config_id}
            )
            row = result.fetchone()
            if not row:
                return None
            return {
                'currency': row[0],
                'base_config': json.loads(row[1]),
                'param_ranges': json.loads(row[2])
            }

    def get_training_results(self, config_id):
        """获取指定配置的所有训练结果"""
        with self.engine.connect() as conn:
            result = conn.execute(
                text("""
                SELECT currency, parameters, result 
                FROM dca_parameter_combinations 
                WHERE config_id = :config_id AND status = 'completed'
                """),
                {'config_id': config_id}
            )
            return [
                {
                    'currency': row[0],
                    'parameters': json.loads(row[1]),
                    'result': json.loads(row[2])
                }
                for row in result.fetchall()
            ]

    def find_best_parameters(self, config_id, metric='sharpe_ratio'):
        """找出表现最好的参数组合"""
        results = self.get_training_results(config_id)
        if not results:
            return None

        best_result = max(
            results,
            key=lambda x: x['result']['performance'][metric] if metric in x['result']['performance'] else float('-inf')
        )
        return best_result


def run_distributed_training_worker(worker_id, db_config, config_id, start_time, end_time):
    """分布式训练工作进程，处理待训练的参数组合"""
    system = ParameterTrainingSystem(db_config)
    config_details = system.get_config_details(config_id)
    if not config_details:
        print(f"配置ID {config_id} 不存在")
        return

    currency = config_details['currency']
    base_config = config_details['base_config']

    # 持续获取并处理待训练的任务
    while True:
        tasks = system.get_pending_tasks(limit=5, currency=currency)
        if not tasks:
            print(f"Worker {worker_id}: 没有更多待处理的任务")
            break

        for task in tasks:
            combination_id = task['combination_id']
            task_currency = task['currency']
            parameters = task['parameters']

            # 标记任务为运行中
            system.mark_task_status(combination_id, 'running', worker_id=worker_id)

            try:
                # 合并基础配置和当前参数
                config = base_config.copy()
                config.update(parameters)
                # 将币种添加到配置中
                config['currency'] = task_currency

                # 运行策略
                result = run_strategy(
                    db_config=db_config,
                    config=config,
                    start_time=start_time,
                    end_time=end_time
                )

                # 标记任务为已完成
                system.mark_task_status(combination_id, 'completed', result=result)
                print(f"Worker {worker_id}: 任务 {combination_id} ({task_currency}) 已完成")
            except Exception as e:
                # 标记任务为失败
                error_msg = str(e)
                system.mark_task_status(combination_id, 'failed', result={'error': error_msg})
                print(f"Worker {worker_id}: 任务 {combination_id} ({task_currency}) 失败: {error_msg}")


def main():
    # 配置数据库连接信息
    db_config = {
        'host': '192.168.123.11',
        'user': 'root',
        'password': 'qwe12345',
        'database': 'trading_db',
        'port': 3306
    }

    # 初始化参数训练系统
    system = ParameterTrainingSystem(db_config)

    # 配置数据时间范围
    end_time = datetime.now()
    start_time = end_time - pd.Timedelta(days=90)

    # 定义要测试的多个币种及其参数配置
    currencies = {
        "BTC": {
            'base_config': {
                'price_drop_threshold': 0.02,
                'max_time_since_last_trade': 96,
                'min_time_since_last_trade': 24,
                'take_profit_threshold': 0.01,
                'initial_capital': 100000,
                'initial_investment_ratio': 0.1,
                'initial_dca_value': 0.035
            },
            'param_ranges': {
                'price_drop_threshold': [0.01, 0.015, 0.02, 0.025, 0.03],
                'max_time_since_last_trade': [24, 48, 72, 96],
                'min_time_since_last_trade': [6, 12, 24, 36],
                'take_profit_threshold': [0.005, 0.01, 0.015],
                'initial_investment_ratio': [0.05, 0.1, 0.15, 0.2],
                'initial_dca_value': [0.02, 0.025, 0.03, 0.035]
            }
        },
        "SUI": {
            'base_config': {
                'price_drop_threshold': 0.03,
                'max_time_since_last_trade': 72,
                'min_time_since_last_trade': 12,
                'take_profit_threshold': 0.015,
                'initial_capital': 50000,
                'initial_investment_ratio': 0.15,
                'initial_dca_value': 0.04
            },
            'param_ranges': {
                'price_drop_threshold': [0.02, 0.025, 0.03, 0.035, 0.04],
                'max_time_since_last_trade': [24, 48, 72, 96],
                'min_time_since_last_trade': [6, 12, 24, 36],
                'take_profit_threshold': [0.01, 0.015, 0.02, 0.025],
                'initial_investment_ratio': [0.1, 0.15, 0.2, 0.25],
                'initial_dca_value': [0.03, 0.035, 0.04, 0.045]
            }
        },

    }

    # 为每个币种保存参数配置到数据库
    config_ids = {}
    for currency, params in currencies.items():
        config_id = system.save_parameters_for_training(
            config_name=f"{currency} DCA策略参数优化",
            currency=currency,
            base_config=params['base_config'],
            param_ranges=params['param_ranges']
        )
        config_ids[currency] = config_id
        print(f"{currency} 参数配置已保存，配置ID: {config_id}")

    # 本地多进程分布式训练示例
    with Pool(processes=4) as pool:
        worker_func = partial(
            run_distributed_training_worker,
            db_config=db_config,
            start_time=start_time,
            end_time=end_time
        )

        # 为每个币种启动工作进程
        worker_args = [(f"{currency}-worker-{i}", config_id)
                       for currency, config_id in config_ids.items()
                       for i in range(2)]  # 每个币种使用2个工作进程

        list(tqdm(pool.starmap(worker_func, worker_args), total=len(worker_args)))

    # 获取每个币种的最佳参数组合
    for currency, config_id in config_ids.items():
        best_result = system.find_best_parameters(config_id)

        if best_result:
            print(f"\n{currency} 参数训练完成!")
            print("最佳参数配置:")
            for key, value in best_result['parameters'].items():
                print(f"{key}: {value}")

            print("\n最佳策略表现:")
            for key, value in best_result['result']['performance'].items():
                print(f"{key}: {value}")
        else:
            print(f"\n{currency}: 没有找到有效的训练结果")


if __name__ == "__main__":
    main()
