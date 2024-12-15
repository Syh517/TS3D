import os
import logging
import pymysql
from locust import HttpUser, between, task
from pymysql.cursors import DictCursor
from pymysql.err import MySQLError
import random
import string
from datetime import datetime

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
        self.node="172.18.0.2:30007"
        self.db_conn = self.create_db_connection()

    def on_stop(self):
        # 在用户生命周期结束时关闭数据库连接
        if hasattr(self, 'db_conn') and self.db_conn is not None:
            self.db_conn.close()

    def get_config(self, key, default):
        return os.getenv(key, default)

    def create_db_connection(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
            try:
                conn = pymysql.connect(
                    host=self.get_config("DB_HOST", "172.18.0.2"),
                    port=int(self.get_config("DB_PORT", 30007)),
                    user=self.get_config("DB_USER", "root"),
                    password=self.get_config("DB_PASSWORD", ""),
                    database="taxi",
                    charset="utf8mb4",
                    cursorclass=DictCursor
                )
                now = datetime.now()
                log="数据库连接成功"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                logger.info("数据库连接成功")
                return conn
            except MySQLError as e:
                now = datetime.now()
                log="数据库连接失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{e}]\n")
                logger.error(f"数据库连接失败: {e}")
                return None

    @task
    def select_drivers(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接过多"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}]\n")
                logger.error("数据库连接过多")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql = "SELECT * FROM drivers LIMIT 1000"
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log="driver数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info(f"driver数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log="未查询到driver数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info("未查询到driver数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except OSError as os_err:
                now = datetime.now()
                log="driver数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log="driver数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{e}]\n")
                logger.error(f"driver数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")


    @task
    def select_users(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接过多"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}]\n")
                logger.error("数据库连接过多")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql = "SELECT * FROM users LIMIT 1000"
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log="user数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info(f"user数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log="未查询到user数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info("未查询到user数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except OSError as os_err:
                now = datetime.now()
                log="user数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log="user数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{e}]\n")
                logger.error(f"user数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")

    
    @task
    def select_orders(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接过多"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}]\n")
                logger.error("数据库连接过多")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql = "SELECT * FROM orders LIMIT 1000"
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log="order数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info(f"order数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log="未查询到order数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info("未查询到order数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except OSError as os_err:
                now = datetime.now()
                log="order数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log="order数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{e}]\n")
                logger.error(f"order数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")

    @task
    def select_payments(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接过多"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}]\n")
                logger.error("数据库连接过多")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql = "SELECT * FROM payments LIMIT 1000"
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log="payment数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info(f"payment数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log="未查询到payment数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][info][{log}]\n")
                        logger.info("未查询到payment数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except OSError as os_err:
                now = datetime.now()
                log="payment数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log="payment数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_frequency][error][{log}][{e}]\n")
                logger.error(f"payment数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_frequency\t'{sql}'\t1\n")


