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
    
    @task(2)
    def insert_driver(self):
        # 执行数据库插入测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 插入数据的 SQL 语句
                sql = "INSERT INTO `drivers` (`name`, `phone`, `license_number`) VALUES (%s, %s, %s)"

                # 生成随机的插入数据
                cursor.execute("SELECT * FROM drivers ORDER BY RAND() LIMIT 1")
                result=cursor.fetchone()
                name=result['name']
                phone =result['phone']
                license_number = result['license_number']
                data = (name, phone, license_number)

                # 执行插入操作
                cursor.execute(sql, data)
                if cursor.rowcount == 0:
                    logger.error(f"driver插入失败")
                else:
                    logger.info(f"driver插入成功: {data}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"driver插入失败: {e}")
            self.db_conn.rollback()



    @task(4)
    def insert_user(self):
        # 执行数据库插入测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 插入数据的 SQL 语句
                sql = "INSERT INTO `users` (`name`, `phone`, `email`) VALUES (%s, %s, %s)"

                # 生成随机的插入数据
                cursor.execute("SELECT * FROM users ORDER BY RAND() LIMIT 1")
                result=cursor.fetchone()
                name=result['name']
                phone =result['phone']
                email = result['email']
                data = (name,phone,email)

                # 执行插入操作
                cursor.execute(sql, data)
                if cursor.rowcount == 0:
                    logger.error(f"user插入失败")
                else:
                    logger.info(f"user插入成功: {data}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"user插入失败: {e}")
            self.db_conn.rollback()

    #重复插入order不会引起问题
    # @task(5)
    def insert_order(self):
        # 执行数据库插入测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 插入数据的 SQL 语句
                sql = "INSERT INTO orders (user_id, driver_id, pickup_location, dropoff_location, status) VALUES (%s, %s, %s, %s, %s)"

                # 生成随机的插入数据
                cursor.execute("SELECT * FROM orders ORDER BY RAND() LIMIT 1")
                result=cursor.fetchone()
                user_id=result['user_id']
                driver_id=result['driver_id']
                pickup_location = result['pickup_location']
                dropoff_location = result['dropoff_location']
                status = result['status']
                data = (user_id, driver_id, pickup_location, dropoff_location, status)

                # 执行插入操作
                cursor.execute(sql, data)
                if cursor.rowcount == 0:
                    logger.error(f"order插入失败")
                else:
                    logger.info(f"order插入成功: {data}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"order插入失败: {e}")
            self.db_conn.rollback()

    @task(5)
    def insert_payment(self):
        # 执行数据库插入测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 插入数据的 SQL 语句
                sql = "INSERT INTO payments (order_id, fare, payment_method, status) VALUES (%s, %s, %s, %s)"

                # 生成随机数据
                cursor.execute("SELECT * FROM payments ORDER BY RAND() LIMIT 1")
                result=cursor.fetchone()
                order_id=result['order_id']
                fare = result['fare']
                payment_method = result['payment_method']
                status = result['status']
                data = (order_id, fare, payment_method, status)

                # 执行插入操作
                cursor.execute(sql, data)
                if cursor.rowcount == 0:
                    logger.error(f"payment插入失败")
                else:
                    logger.info(f"payment插入成功: {data}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"payment插入失败: {e}")
            self.db_conn.rollback()






