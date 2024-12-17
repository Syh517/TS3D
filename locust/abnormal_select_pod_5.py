import os
import logging
import pymysql
from locust import HttpUser, between, task
from pymysql.cursors import DictCursor
from pymysql.err import MySQLError
import random
import string
from datetime import datetime
import re

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
        self.node="10.244.0.26:3306"
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
                    port=int(self.get_config("DB_PORT", 30889)),
                    user=self.get_config("DB_USER", "root"),
                    password=self.get_config("DB_PASSWORD", ""),
                    database="taxi",
                    charset="utf8mb4",
                    cursorclass=DictCursor
                )
                now = datetime.now()
                log="数据库连接成功"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                logger.info("数据库连接成功")
                return conn
            except MySQLError as e:
                now = datetime.now()
                log="数据库连接失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"数据库连接失败: {e}")
                return None

    @task
    def select_1(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")


    @task
    def select_2(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")


    @task
    def select_3(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")


    @task
    def select_4(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")


    @task
    def select_5(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            function_name = "select_5"
            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql ='''SELECT user_id, COUNT(*) AS order_count
                            FROM orders
                            GROUP BY user_id;'''
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")


    @task
    def select_6(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            function_name = "select_6"
            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql ='''SELECT driver_id, COUNT(*) AS order_count
                            FROM orders
                            GROUP BY driver_id;'''
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")



    @task
    def select_7(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")



    @task
    def select_8(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")



    @task
    def select_9(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            function_name = "select_9"
            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql ="SELECT SUM(fare) AS total_amount FROM payments;"

                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")


    @task
    def select_10(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")



    @task
    def select_11(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")


    @task
    def select_12(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            function_name = "select_12"
            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql ="SELECT AVG(fare) AS average_amount FROM payments;"

                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")


    @task
    def select_13(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")


    @task
    def select_14(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")


    @task
    def select_15(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            function_name = "select_15"
            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql ="SELECT MAX(fare) AS max_amount FROM payments;"

                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")


    @task
    def select_16(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            function_name = "select_16"
            try:
                with self.db_conn.cursor() as cursor:
                    # 查询数据的 SQL 语句
                    sql ="SELECT MIN(fare) AS min_amount FROM payments;"

                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql}'\t1\n")



    @task
    def select_17(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")



    @task
    def select_18(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")


    @task
    def select_19(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")


    @task
    def select_20(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}]\n")
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
                    sql0=re.sub(r'\s+', ' ', sql).strip()
                    
                    # 执行查询操作
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        now = datetime.now()
                        log=f"{function_name}数据查询成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"{function_name}数据查询成功")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"未查询到{function_name}数据"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][info][{log}]\n")
                        logger.info(f"未查询到{function_name}数据")
                        file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")
            except MySQLError as e:
                now = datetime.now()
                log=f"{function_name}数据查询失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_select_pod_5][error][{log}][{e}]\n")
                logger.error(f"{function_name}数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tabnormal_select_pod_5\t'{sql0}'\t1\n")



