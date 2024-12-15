import os
import logging
import pymysql
from locust import HttpUser, between, task
from pymysql.cursors import DictCursor
from pymysql.err import MySQLError
import random
import string
from faker import Faker
from datetime import datetime
import re

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
        self.node="10.244.0.30:3306"
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
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][info][{log}]\n")
                logger.info("数据库连接成功")
                return conn
            except MySQLError as e:
                now = datetime.now()
                log="数据库连接失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}][{e}]\n")
                logger.error(f"数据库连接失败: {e}")
                return None
    
    @task(2)
    def insert_driver(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库插入测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 插入数据的 SQL 语句
                    sql = "INSERT INTO drivers (name, phone, license_number) VALUES (%s, %s, %s)"

                    # 生成随机的插入数据
                    cursor.execute("SELECT * FROM drivers ORDER BY RAND() LIMIT 1")
                    result=cursor.fetchone()
                    name=result['name']
                    phone =result['phone']
                    license_number = result['license_number']
                    data = (name, phone, license_number)

                    # 执行插入操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"driver插入失败: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                        logger.error(f"driver插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"driver插入成功: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][info][{log}]\n")
                        logger.info(f"driver插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="driver插入失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}][{e}]\n")
                logger.error(f"driver插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")



    @task(3)
    def insert_user(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库插入测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 插入数据的 SQL 语句
                    sql = "INSERT INTO users (name, phone, email) VALUES (%s, %s, %s)"

                    # 生成随机的插入数据
                    cursor.execute("SELECT * FROM users ORDER BY RAND() LIMIT 1")
                    result=cursor.fetchone()
                    name=result['name']
                    phone =result['phone']
                    email = result['email']
                    data = (name,phone,email)

                    # 执行插入操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"user插入失败: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                        logger.error(f"user插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"user插入成功: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][info][{log}]\n")
                        logger.info(f"user插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="user插入失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}][{e}]\n")
                logger.error(f"user插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")


    #重复插入order不会引起问题
    # @task(5)
    def insert_order(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库插入测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
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
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"order插入失败: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                        logger.error(f"order插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"order插入成功: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][info][{log}]\n")
                        logger.info(f"order插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="order插入失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}][{e}]\n")
                logger.error(f"order插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")

    @task(5)
    def insert_order_2(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库插入测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 插入数据的 SQL 语句
                    sql = "INSERT INTO orders (user_id, driver_id, pickup_location, dropoff_location, status) VALUES (%s, %s, %s, %s, %s)"

                    # 生成随机的插入数据
                    user_id='1'
                    driver_id='1'
                    address1 = fake.address()
                    address2 = fake.address()
                    while address1 == address2:
                        address2 = fake.address()
                    pickup_location=re.sub(r'\s+', ' ', address1).strip()
                    dropoff_location=re.sub(r'\s+', ' ', address2).strip()
                    status = random.choice(['pending', 'accepted', 'completed', 'cancelled'])
                    data = (user_id, driver_id, pickup_location, dropoff_location, status)

                    # 执行插入操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"order插入失败: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                        logger.error(f"order插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"order插入成功: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][info][{log}]\n")
                        logger.info(f"order插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="order插入失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}][{e}]\n")
                logger.error(f"order插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")

    @task(5)
    def insert_payment(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库插入测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
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
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"payment插入失败: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                        logger.error(f"payment插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"payment插入成功: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][info][{log}]\n")
                        logger.info(f"payment插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="payment插入失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}][{e}]\n")
                logger.error(f"payment插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")



    @task(5)
    def insert_payment_2(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库插入测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 插入数据的 SQL 语句
                    sql = "INSERT INTO payments (order_id, fare, payment_method, status) VALUES (%s, %s, %s, %s)"

                    # 生成随机数据
                    order_id='1'
                    fare = round(random.uniform(10, 100), 2)
                    payment_method = random.choice(['credit_card', 'debit_card', 'cash'])
                    status = random.choice(['pending', 'completed', 'failed'])
                    data = (order_id, fare, payment_method, status)

                    # 执行插入操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"payment插入失败: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}]\n")
                        logger.error(f"payment插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                    else:
                        now = datetime.now()
                        log=f"payment插入成功: {data}"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][info][{log}]\n")
                        logger.info(f"payment插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="payment插入失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_insert][error][{log}][{e}]\n")
                logger.error(f"payment插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tabnormal_insert\t'{sql0}'\t1\n")




