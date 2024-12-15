import os
import logging
import pymysql
from locust import HttpUser, between, task
from pymysql.cursors import DictCursor
from pymysql.err import MySQLError
import random
import string
from faker import Faker
import requests
from datetime import datetime

fake = Faker()

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
        self.node="10.244.0.17:3306"
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
                    host=self.get_config("DB_HOST", "127.0.0.1"),
                    port=int(self.get_config("DB_PORT", 3306)),
                    user=self.get_config("DB_USER", "root"),
                    password=self.get_config("DB_PASSWORD", ""),
                    database="taxi",
                    charset="utf8mb4",
                    cursorclass=DictCursor
                )
                now = datetime.now()
                log="数据库连接成功"
                file.write(f"[{self.node}][{now}][info][{log}]\n")
                logger.info("数据库连接成功")          
                return conn
            except MySQLError as e:
                now = datetime.now()
                log="数据库连接失败"
                file.write(f"[{self.node}][{now}][error][{log}][{e}]\n")
                logger.error(f"数据库连接失败: {e}")
                return None
    



    @task(2)
    def insert_driver(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 插入数据的 SQL 语句
                    sql = "INSERT INTO drivers (name, phone, license_number) VALUES (%s, %s, %s)"

                    # 生成随机的插入数据
                    drivername=fake.name()
                    phone = fake.phone_number()
                    license_number = fake.license_plate()
                    data = (drivername, phone, license_number)

                    # 执行插入操作
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"driver插入失败: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"driver插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t1\t'{sql}'\n")
                    else:
                        now = datetime.now()
                        log=f"driver插入成功: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"driver插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'{sql}'\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="driver插入失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"driver插入失败: {e}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t1\t'{sql}'\n")
                self.db_conn.rollback()