import os
import logging
import pymysql
from locust import HttpUser, between, task
from pymysql.cursors import DictCursor
from pymysql.err import MySQLError
import random
import string
from faker import Faker

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
                host=self.get_config("DB_HOST", "127.0.0.1"),
                port=int(self.get_config("DB_PORT", 3306)),
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
    def update_1(self):
        # 执行数据库更新测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:

                # 更新数据的 SQL 语句
                sql1 ="SELECT * FROM drivers WHERE driver_id = 4 FOR UPDATE;"
                sql2 ="SELECT SLEEP(2)"
                sql3 ="UPDATE drivers SET license_number = %s WHERE driver_id = 4"
                
                sql4 ="UPDATE drivers SET license_number = %s WHERE driver_id = 5"

                        

                # 生成随机的更新数据
                license1=fake.license_plate()
                license2=fake.license_plate()

                # 执行更新操作
                cursor.execute(sql1)
                if cursor.rowcount == 0:
                    logger.error(f"update_1_sql1执行失败")
                else:
                    logger.info(f"update_1_sql1执行成功")

                cursor.execute(sql2)
                if cursor.rowcount == 0:
                    logger.error(f"update_1_sql2执行失败")
                else:
                    logger.info(f"update_1_sql2执行成功")

                cursor.execute(sql3, license1)
                if cursor.rowcount == 0:
                    logger.error(f"update_1_sql3执行失败")
                else:
                    logger.info(f"update_1_sql3执行成功")

                cursor.execute(sql4, license2)
                if cursor.rowcount == 0:
                    logger.error(f"update_1_sql4执行失败")
                else:
                    logger.info(f"update_1_sql4执行成功")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"update_1更新失败: {e}")
            self.db_conn.rollback()

    @task
    def update_2(self):
        # 执行数据库更新测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:

                # 更新数据的 SQL 语句
                sql1 ="SELECT * FROM users WHERE user_id = 2 FOR UPDATE;"
                sql2 ="SELECT SLEEP(2)"
                sql3 ="UPDATE users SET email = %s WHERE user_id = 2"
                
                sql4 ="UPDATE users SET email = %s WHERE user_id = 3"

                        

                # 生成随机的更新数据
                email1=fake.email()
                email2=fake.email()

                # 执行更新操作
                cursor.execute(sql1)
                if cursor.rowcount == 0:
                    logger.error(f"update_2_sql1执行失败")
                else:
                    logger.info(f"update_2_sql1执行成功")

                cursor.execute(sql2)
                if cursor.rowcount == 0:
                    logger.error(f"update_2_sql2执行失败")
                else:
                    logger.info(f"update_2_sql2执行成功")

                cursor.execute(sql3, email1)
                if cursor.rowcount == 0:
                    logger.error(f"update_2_sql3执行失败")
                else:
                    logger.info(f"update_2_sql3执行成功")

                cursor.execute(sql4, email2)
                if cursor.rowcount == 0:
                    logger.error(f"update_2_sql4执行失败")
                else:
                    logger.info(f"update_2_sql4执行成功")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"update_2更新失败: {e}")
            self.db_conn.rollback()

    @task(2)
    def update_3(self):
        # 执行数据库更新测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:

                # 更新数据的 SQL 语句
                sql1 ="SELECT * FROM drivers WHERE driver_id = 5 FOR UPDATE;"
                sql2 ="SELECT SLEEP(2)"
                sql3 ="UPDATE drivers SET license_number = %s WHERE driver_id = 5"
                
                sql4 ="UPDATE drivers SET license_number = %s WHERE driver_id = 4"

                        

                # 生成随机的更新数据
                license1=fake.license_plate()
                license2=fake.license_plate()

                # 执行更新操作
                cursor.execute(sql1)
                if cursor.rowcount == 0:
                    logger.error(f"update_3_sql1执行失败")
                else:
                    logger.info(f"update_3_sql1执行成功")

                cursor.execute(sql2)
                if cursor.rowcount == 0:
                    logger.error(f"update_3_sql2执行失败")
                else:
                    logger.info(f"update_3_sql2执行成功")

                cursor.execute(sql3, license1)
                if cursor.rowcount == 0:
                    logger.error(f"update_3_sql3执行失败")
                else:
                    logger.info(f"update_3_sql3执行成功")

                cursor.execute(sql4, license2)
                if cursor.rowcount == 0:
                    logger.error(f"update_3_sql4执行失败")
                else:
                    logger.info(f"update_3_sql4执行成功")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"update_3更新失败: {e}")
            self.db_conn.rollback()
    

    @task(2)
    def update_4(self):
        # 执行数据库更新测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:

                # 更新数据的 SQL 语句
                sql1 ="SELECT * FROM users WHERE user_id = 3 FOR UPDATE;"
                sql2 ="SELECT SLEEP(2)"
                sql3 ="UPDATE users SET email = %s WHERE user_id = 3"
                
                sql4 ="UPDATE users SET email = %s WHERE user_id = 2"

                        

                # 生成随机的更新数据
                email1=fake.email()
                email2=fake.email()

                # 执行更新操作
                cursor.execute(sql1)
                if cursor.rowcount == 0:
                    logger.error(f"update_4_sql1执行失败")
                else:
                    logger.info(f"update_4_sql1执行成功")

                cursor.execute(sql2)
                if cursor.rowcount == 0:
                    logger.error(f"update_4_sql2执行失败")
                else:
                    logger.info(f"update_4_sql2执行成功")

                cursor.execute(sql3, email1)
                if cursor.rowcount == 0:
                    logger.error(f"update_4_sql3执行失败")
                else:
                    logger.info(f"update_4_sql3执行成功")

                cursor.execute(sql4, email2)
                if cursor.rowcount == 0:
                    logger.error(f"update_4_sql4执行失败")
                else:
                    logger.info(f"update_4_sql4执行成功")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"update_4更新失败: {e}")
            self.db_conn.rollback()









