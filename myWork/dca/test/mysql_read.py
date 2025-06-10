import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pymysql
import random
import multiprocessing
from functools import lru_cache
from cachetools import TTLCache
from cachetools.keys import hashkey


class MySQLDataReader:
    def __init__(self, host, user, password, database, port=3306, charset='utf8mb4', cache_maxsize=10, cache_ttl=3600):
        """
        初始化数据库连接参数

        参数:
        host: 数据库主机地址
        user: 数据库用户名
        password: 数据库密码
        database: 数据库名称
        port: 数据库端口，默认为3306
        charset: 字符集，默认为utf8mb4
        cache_maxsize: 缓存最多存储的数据集数量
        cache_ttl: 缓存数据的有效时间(秒)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.connection = None
        self.cache = TTLCache(maxsize=cache_maxsize, ttl=cache_ttl)
        # 使用进程锁替代线程锁
        self.lock = multiprocessing.RLock()

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"成功连接到数据库: {self.database}")
        except Exception as e:
            print(f"连接数据库失败: {e}")
            raise

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            print("已断开数据库连接")

    def execute_query(self, query, params=None):
        """执行SQL查询并返回结果"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"执行查询失败: {e}")
            raise

    def get_sorted_history_data(self, start_time=None, end_time=None, currency=None, limit=None):
        """
        获取sorted_history表中的数据，支持多进程缓存读取

        参数:
        start_time: 开始时间，默认为None，表示不限制
        end_time: 结束时间，默认为None，表示不限制
        currency: 币种，默认为None，表示不限制
        limit: 返回记录数限制，默认为None，表示不限制

        返回:
        pandas DataFrame格式的数据
        """
        # 生成缓存键
        key = hashkey(start_time, end_time, currency, limit)

        # 进程安全的缓存读取
        with self.lock:
            if key in self.cache:
                print(f"从缓存获取数据: start={start_time}, end={end_time}, currency={currency}, limit={limit}")
                return self.cache[key].copy()  # 返回副本，避免修改缓存数据

            # 缓存未命中，从数据库读取
            query = "SELECT * FROM sorted_history_sui"
            conditions = []
            params = []

            if start_time:
                conditions.append("ts >= %s")
                params.append(start_time)

            if end_time:
                conditions.append("ts <= %s")
                params.append(end_time)

            # if currency:
            #     conditions.append("currency = %s")  # 添加币种条件
            #     params.append(currency)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY ts ASC"

            if limit:
                query += f" LIMIT {limit}"

            result = self.execute_query(query, params)

            # 转换为DataFrame
            df = pd.DataFrame(result)

            # 确保ts列是datetime类型
            if 'ts' in df.columns:
                df['ts'] = pd.to_datetime(df['ts'])

            # 缓存数据
            self.cache[key] = df.copy()  # 存储副本，避免外部修改
            print(f"已缓存数据: start={start_time}, end={end_time}, currency={currency}, limit={limit}")

            return df

    def clear_cache(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            print("缓存已清空")

    def get_cache_info(self):
        """获取缓存信息"""
        with self.lock:
            return {
                'current_size': len(self.cache),
                'max_size': self.cache.maxsize,
                'ttl': self.cache.ttl
            }