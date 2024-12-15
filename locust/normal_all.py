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
                file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                logger.info("数据库连接成功")
                return conn
            except MySQLError as e:
                now = datetime.now()
                log="数据库连接失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
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
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"driver插入失败: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"driver插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"driver插入成功: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"driver插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="driver插入失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"driver插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def update_driver(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 更新数据的 SQL 语句
                    sql = "UPDATE drivers SET license_number = %s WHERE driver_id = %s"

                    # 生成随机的更新数据
                    cursor.execute("SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有driver数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有driver数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1'\n")
                        return
                    driver_id = cursor.fetchone()['driver_id']
                    license_number = fake.license_plate()
                    data=(license_number, driver_id)

                    # 执行更新操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"driver更新失败:请为{driver_id}用户设置与原数据不同的信息"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"driver更新失败:请为{driver_id}用户设置与原数据不同的信息")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"driver更新成功: {license_number}, {driver_id}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"driver更新成功: {license_number}, {driver_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="driver更新失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"driver更新失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def delete_driver(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 删除数据的 SQL 语句
                    sql = "DELETE FROM drivers WHERE driver_id = %s"

                    # 生成随机的删除数据
                    cursor.execute("SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有driver数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有driver数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1'\n")
                        return
                    driver_id = cursor.fetchone()['driver_id']
                    data=(driver_id,)

                    # 执行删除操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"driver删除失败:driver_id为{driver_id}"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"driver删除失败:driver_id为{driver_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"driver删除成功: {driver_id}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"driver删除成功: {driver_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="driver删除失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"driver删除失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")


    @task(2)
    def insert_user(self):
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
                    sql = "INSERT INTO users (name, phone, email) VALUES (%s, %s, %s)"

                    # 生成随机的插入数据
                    username=fake.name()
                    phone = fake.phone_number()
                    email = fake.email()
                    data = (username,phone,email)

                    # 执行插入操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"user插入失败: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"user插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"user插入成功: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"user插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="user插入失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"user插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def update_user(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 更新数据的 SQL 语句
                    sql = "UPDATE users SET email = %s WHERE user_id = %s"

                    # 生成随机的更新数据
                    cursor.execute("SELECT user_id FROM users ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有user数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有user数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT user_id FROM users ORDER BY RAND() LIMIT 1'\n")
                        return
                    user_id = cursor.fetchone()['user_id']
                    email = fake.email()
                    data=(email, user_id)

                    # 执行更新操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"user更新失败:请为{user_id}用户设置与原数据不同的信息"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"user更新失败:请为{user_id}用户设置与原数据不同的信息")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"user更新成功: {email}, {user_id}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"user更新成功: {email}, {user_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="user更新失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"user更新失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def delete_user(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 删除数据的 SQL 语句
                    sql = "DELETE FROM users WHERE user_id = %s"

                    # 生成随机的删除数据
                    cursor.execute("SELECT user_id FROM users ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有user数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有user数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT user_id FROM users ORDER BY RAND() LIMIT 1'\n")
                        return
                    user_id = cursor.fetchone()['user_id']
                    data=(user_id,)

                    # 执行删除操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"user删除失败:user_id为{user_id}"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"user删除失败:user_id为{user_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"user删除成功: {user_id}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"user删除成功: {user_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="user删除失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"user删除失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(2)
    def insert_order(self):
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
                    sql = "INSERT INTO orders (user_id, driver_id, pickup_location, dropoff_location, status) VALUES (%s, %s, %s, %s, %s)"
                    
                    # 获取随机的 user_id 和 driver_id
                    cursor.execute("SELECT user_id FROM users ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有user数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有user数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT user_id FROM users ORDER BY RAND() LIMIT 1'\n")
                        return
                    user_id = cursor.fetchone()['user_id']

                    cursor.execute("SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有driver数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有driver数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1'\n")
                        return
                    driver_id = cursor.fetchone()['driver_id']

                    # 生成随机的插入数据
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
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"order插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"order插入成功: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"order插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="order插入失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"order插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def update_order(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 更新数据的 SQL 语句
                    sql = "UPDATE orders SET status = %s WHERE order_id = %s"

                    # 生成随机的更新数据
                    cursor.execute("SELECT order_id, status FROM orders ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有order数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有order数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT order_id, status FROM orders ORDER BY RAND() LIMIT 1'\n")
                        return
                    result_0 = cursor.fetchone() #此函数只能调用一次
                    order_id = result_0['order_id']
                    status = result_0['status']
                    data0 = (status, order_id)
                    sql0=sql%data0

                    if status != 'completed' and status != 'cancelled':
                        if status == 'pending':
                            status = 'accepted'
                        elif status == 'accepted':
                            status = random.choice(['completed', 'cancelled'])

                        data = (status, order_id)

                        # 执行更新操作
                        sql0=sql%data
                        cursor.execute(sql, data)
                        if cursor.rowcount == 0:
                            now = datetime.now()
                            log=f"order更新失败:数据库不存在order_id为{order_id}的数据"
                            file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                            logger.error(f"order更新失败:数据库不存在order_id为{order_id}的数据")
                            file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                        else:
                            now = datetime.now()
                            log=f"order更新成功: {status}, {order_id}"
                            file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                            logger.info(f"order更新成功: {status}, {order_id}")
                            file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="order更新失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"order更新失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def delete_order(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 删除数据的 SQL 语句
                    sql = "DELETE FROM orders WHERE order_id = %s"

                    # 生成随机的删除数据
                    order_id = random.randint(1, 100)  
                    cursor.execute("SELECT order_id FROM orders ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有order数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有order数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT order_id FROM orders ORDER BY RAND() LIMIT 1'\n")
                        return
                    order_id = cursor.fetchone()['order_id']
                    data=(order_id,)

                    # 执行删除操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"order删除失败:order_id为{order_id}"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"order删除失败:order_id为{order_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"order删除成功: {order_id}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"order删除成功: {order_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="order删除失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"order删除失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(2)
    def insert_payment(self):
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
                    sql = "INSERT INTO payments (order_id, fare, payment_method, status) VALUES (%s, %s, %s, %s)"

                    # 获取随机的 order_id
                    cursor.execute("SELECT order_id FROM orders WHERE status = 'completed' ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有order数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有order数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT order_id FROM orders WHERE status = 'completed' ORDER BY RAND() LIMIT 1'\n")
                        return
                    order_id = cursor.fetchone()['order_id']

                    # 生成随机数据
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
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"payment插入失败: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"payment插入成功: {data}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"payment插入成功: {data}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="payment插入失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"payment插入失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def update_payment(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 更新数据的 SQL 语句
                    sql = "UPDATE payments SET status = %s WHERE payment_id = %s"

                    # 生成随机的更新数据
                    cursor.execute("SELECT payment_id, status FROM payments ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有payment数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有payment数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT payment_id, status FROM payments ORDER BY RAND() LIMIT 1'\n")
                        return
                    result_0 = cursor.fetchone() #此函数只能调用一次
                    payment_id = result_0['payment_id']
                    status = result_0['status']
                    data0 = (status, payment_id)
                    sql0=sql%data0

                    if status == 'pending':
                        status = random.choice(['completed', 'failed'])

                        data=(status, payment_id)

                        # 执行更新操作
                        sql0=sql%data
                        cursor.execute(sql, data)
                        if cursor.rowcount == 0:
                            now = datetime.now()
                            log=f"payment更新失败:数据库不存在payment_id为{payment_id}的数据"
                            file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                            logger.error(f"payment更新失败:数据库不存在payment_id为{payment_id}的数据")
                            file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                        else:
                            now = datetime.now()
                            log=f"payment更新成功: {status}, {payment_id}"
                            file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                            logger.info(f"payment更新成功: {status}, {payment_id}")
                            file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="payment更新失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"payment更新失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(1)
    def delete_payment(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    # 删除数据的 SQL 语句
                    sql = "DELETE FROM payments WHERE payment_id = %s"

                    # 生成随机的删除数据
                    cursor.execute("SELECT payment_id FROM payments ORDER BY RAND() LIMIT 1")
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log="没有payment数据"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error("没有payment数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t0\t'SELECT payment_id FROM payments ORDER BY RAND() LIMIT 1'\n")
                        return
                    payment_id = cursor.fetchone()['payment_id']
                    data=(payment_id,)

                    # 执行删除操作
                    sql0=sql%data
                    cursor.execute(sql, data)
                    if cursor.rowcount == 0:
                        now = datetime.now()
                        log=f"payment删除失败:payment_id为{payment_id}"
                        file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                        logger.error(f"payment删除失败:payment_id为{payment_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                    else:
                        now = datetime.now()
                        log=f"payment删除成功: {payment_id}"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"payment删除成功: {payment_id}")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")
                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="payment删除失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"payment删除失败: {e}")
                self.db_conn.rollback()
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql0}'\t0\n")

    @task(6)
    def select_drivers(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
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
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"driver数据查询成功")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
                    else:
                        now = datetime.now()
                        log="未查询到driver数据"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info("未查询到driver数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except OSError as os_err:
                now = datetime.now()
                log="driver数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except MySQLError as e:
                now = datetime.now()
                log="driver数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"driver数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")


    @task(6)
    def select_users(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
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
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"user数据查询成功")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
                    else:
                        now = datetime.now()
                        log="未查询到user数据"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info("未查询到user数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except OSError as os_err:
                now = datetime.now()
                log="user数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except MySQLError as e:
                now = datetime.now()
                log="user数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"user数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")

    
    @task(6)
    def select_orders(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
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
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"order数据查询成功")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
                    else:
                        now = datetime.now()
                        log="未查询到order数据"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info("未查询到order数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except OSError as os_err:
                now = datetime.now()
                log="order数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except MySQLError as e:
                now = datetime.now()
                log="order数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"order数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")

    @task(6)
    def select_payments(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file, open("/home/yyy/mysql/data/logs/sqls.txt",'a') as file2:
            # 执行数据库查询测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}]\n")
                logger.error("数据库连接未初始化")
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
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info(f"payment数据查询成功")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
                    else:
                        now = datetime.now()
                        log="未查询到payment数据"
                        file.write(f"[{now}][{self.node}][normal_all][info][{log}]\n")
                        logger.info("未查询到payment数据")
                        file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except OSError as os_err:
                now = datetime.now()
                log="payment数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{os_err}]\n")
                logger.error(f"OSError: {os_err}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")
            except MySQLError as e:
                now = datetime.now()
                log="payment数据查询失败"
                file.write(f"[{now}][{self.node}][normal_all][error][{log}][{e}]\n")
                logger.error(f"payment数据查询失败: {e}")
                file2.write(f"{now}\t{self.node}\tnormal_all\t'{sql}'\t0\n")