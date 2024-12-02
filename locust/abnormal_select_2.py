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
    def select_1(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_1"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT COUNT(*) AS total_drivers FROM drivers;"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_2(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_2"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT COUNT(*) AS total_users FROM users;"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_3(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_3"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT COUNT(*) AS total_orders FROM orders;"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_4(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_4"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT COUNT(*) AS total_payments FROM payments;"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_5(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_5"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT user_id, COUNT(*) AS order_count
                        FROM orders
                        GROUP BY user_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_6(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_6"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT driver_id, COUNT(*) AS order_count
                        FROM orders
                        GROUP BY driver_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")



    @task
    def select_7(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_7"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.user_id, COUNT(p.payment_id) AS payment_count
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.user_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")



    @task
    def select_8(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_8"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.driver_id, COUNT(p.payment_id) AS payment_count
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.driver_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")



    @task
    def select_9(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_9"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT SUM(fare) AS total_amount FROM payments;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_10(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_10"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.user_id, SUM(p.fare) AS total_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.user_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")



    @task
    def select_11(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_11"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.driver_id, SUM(p.fare) AS total_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.driver_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_12(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_12"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT AVG(fare) AS average_amount FROM payments;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_13(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_13"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.user_id, AVG(p.fare) AS average_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.user_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_14(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_14"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.driver_id, AVG(p.fare) AS average_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.driver_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_15(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_15"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT MAX(fare) AS max_amount FROM payments;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_16(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_16"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT MIN(fare) AS min_amount FROM payments;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")



    @task
    def select_17(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_17"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.user_id, MAX(p.fare) AS max_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.user_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")



    @task
    def select_18(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_18"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.user_id, MIN(p.fare) AS min_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.user_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_19(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_19"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.driver_id, MAX(p.fare) AS max_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.driver_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")


    @task
    def select_20(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        function_name = "select_20"
        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT o.driver_id, MIN(p.fare) AS min_amount
                        FROM orders o
                        JOIN payments p ON o.order_id = p.order_id
                        GROUP BY o.driver_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"{function_name}数据查询成功")
                else:
                    logger.info(f"未查询到{function_name}数据")
        except MySQLError as e:
            logger.error(f"{function_name}数据查询失败: {e}")
































    

