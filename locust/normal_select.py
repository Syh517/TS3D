import os
import logging
import pymysql
from locust import HttpUser, between, task
from pymysql.cursors import DictCursor
from pymysql.err import MySQLError
import random
import string

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://example.com"  # 指定基础主机

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_start(self):
        # 初始化数据库连接
        self.db_conn = self.create_db_connection()

    def on_stop(self):
        # 在用户生命周期结束时关闭数据库连接
        if self.db_conn:
            self.db_conn.close()

    def get_config(self, key, default):
        return os.getenv(key, default)

    def create_db_connection(self):
        try:
            conn = pymysql.connect(
                host=self.get_config("DB_HOST", "172.20.0.2"),
                port=int(self.get_config("DB_PORT", 30007)),
                user=self.get_config("DB_USER", "root"),
                password=self.get_config("DB_PASSWORD", ""),
                database="taxi",
                charset="utf8mb4",
                cursorclass=DictCursor
            )
            logger.info("数据库连接成功")
            return conn
        except MySQLError as e:
            logger.error(f"数据库连接失败: {e}")
            return None

    @task
    def select_drivers(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `drivers` LIMIT 10"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"driver数据查询成功: {result}")
                else:
                    logger.info("未查询到driver数据")
        except MySQLError as e:
            logger.error(f"driver数据查询失败: {e}")


    @task
    def select_users(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `users` LIMIT 10"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"user数据查询成功: {result}")
                else:
                    logger.info("未查询到user数据")
        except MySQLError as e:
            logger.error(f"user数据查询失败: {e}")

    
    @task
    def select_orders(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `orders` LIMIT 10"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"order数据查询成功: {result}")
                else:
                    logger.info("未查询到order数据")
                
        except MySQLError as e:
            logger.error(f"order数据查询失败: {e}")

    @task
    def select_payments(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `payments` LIMIT 10"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"payment数据查询成功: {result}")
                else:
                    logger.info("未查询到payment数据")
        except MySQLError as e:
            logger.error(f"payment数据查询失败: {e}")


