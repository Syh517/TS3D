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
    def call_api(self):
        # 执行数据库更新测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:


                # 调用外部API

                response = requests.get("https://www.iqiyi.com/?vfm=f_588_wrb&fv=ac30238882b84c8c")
                if response.status_code == 200:
                    logger.info(f"调用成功")
                else:
                    logger.error(f"调用失败")


                
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"调用失败: {e}")
            self.db_conn.rollback()