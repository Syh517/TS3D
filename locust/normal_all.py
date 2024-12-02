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
                drivername=fake.name()
                phone = fake.phone_number()
                license_number = fake.license_plate()
                data = (drivername, phone, license_number)

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

    @task(1)
    def update_driver(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 更新数据的 SQL 语句
                sql = "UPDATE `drivers` SET `license_number` = %s WHERE `driver_id` = %s"

                # 生成随机的更新数据
                cursor.execute("SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1")
                driver_id = cursor.fetchone()['driver_id']
                license_number = fake.license_plate()

                # 执行更新操作
                cursor.execute(sql, (license_number, driver_id))
                if cursor.rowcount == 0:
                    logger.error(f"driver更新失败:请为{driver_id}用户设置与原数据不同的信息")
                else:
                    logger.info(f"driver更新成功: {license_number}, {driver_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"driver更新失败: {e}")
            self.db_conn.rollback()

    @task(1)
    def delete_driver(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 删除数据的 SQL 语句
                sql = "DELETE FROM `drivers` WHERE `driver_id` = %s"

                # 生成随机的删除数据
                cursor.execute("SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1")
                driver_id = cursor.fetchone()['driver_id']

                # 执行删除操作
                cursor.execute(sql, (driver_id,))
                if cursor.rowcount == 0:
                    logger.error(f"driver删除失败:driver_id为{driver_id}")
                else:
                    logger.info(f"driver删除成功: {driver_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"driver删除失败: {e}")
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
                username=fake.name()
                phone = fake.phone_number()
                email = fake.email()
                data = (username,phone,email)

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

    @task(1)
    def update_user(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 更新数据的 SQL 语句
                sql = "UPDATE `users` SET `email` = %s WHERE `user_id` = %s"

                # 生成随机的更新数据
                cursor.execute("SELECT user_id FROM users ORDER BY RAND() LIMIT 1")
                user_id = cursor.fetchone()['user_id']
                email = fake.email()

                # 执行更新操作
                cursor.execute(sql, (email, user_id))
                if cursor.rowcount == 0:
                    logger.error(f"user更新失败:请为{user_id}用户设置与原数据不同的信息")
                else:
                    logger.info(f"user更新成功: {email}, {user_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"user更新失败: {e}")
            self.db_conn.rollback()

    @task(1)
    def delete_user(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 删除数据的 SQL 语句
                sql = "DELETE FROM `users` WHERE `user_id` = %s"

                # 生成随机的删除数据
                cursor.execute("SELECT user_id FROM users ORDER BY RAND() LIMIT 1")
                user_id = cursor.fetchone()['user_id']
                # 执行删除操作
                cursor.execute(sql, (user_id,))
                if cursor.rowcount == 0:
                    logger.error(f"user删除失败:user_id为{user_id}")
                else:
                    logger.info(f"user删除成功: {user_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"user删除失败: {e}")
            self.db_conn.rollback()

    @task(5)
    def insert_order(self):
        # 执行数据库插入测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 插入数据的 SQL 语句
                sql = "INSERT INTO orders (user_id, driver_id, pickup_location, dropoff_location, status) VALUES (%s, %s, %s, %s, %s)"
                
                # 获取随机的 user_id 和 driver_id
                cursor.execute("SELECT user_id FROM users ORDER BY RAND() LIMIT 1")
                user_id = cursor.fetchone()['user_id']

                cursor.execute("SELECT driver_id FROM drivers ORDER BY RAND() LIMIT 1")
                driver_id = cursor.fetchone()['driver_id']

                # 生成随机的插入数据
                address1 = fake.address()
                address2 = fake.address()
                while address1 == address2:
                    address2 = fake.address()
                pickup_location = address1
                dropoff_location = address2
                status = random.choice(['pending', 'accepted', 'completed', 'cancelled'])
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

    @task(3)
    def update_order(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 更新数据的 SQL 语句
                sql = "UPDATE `orders` SET `status` = %s WHERE `order_id` = %s"

                # 生成随机的更新数据
                cursor.execute("SELECT order_id, status FROM orders ORDER BY RAND() LIMIT 1")
                result_0 = cursor.fetchone() #此函数只能调用一次
                if result_0 is None:
                    print("没有order数据")
                    return
                order_id = result_0['order_id']
                status = result_0['status']
                if status != 'completed' and status != 'cancelled':
                    if status == 'pending':
                        status = 'accepted'
                    elif status == 'accepted':
                        status = random.choice(['completed', 'cancelled'])

                    # 执行更新操作
                    cursor.execute(sql, (status, order_id))
                    if cursor.rowcount == 0:
                        logger.error(f"order更新失败:数据库不存在order_id为{order_id}的数据")
                    else:
                        logger.info(f"order更新成功: {status}, {order_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"order更新失败: {e}")
            self.db_conn.rollback()

    @task(1)
    def delete_order(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 删除数据的 SQL 语句
                sql = "DELETE FROM `orders` WHERE `order_id` = %s"

                # 生成随机的删除数据
                order_id = random.randint(1, 100)  
                cursor.execute("SELECT order_id FROM orders ORDER BY RAND() LIMIT 1")
                order_id = cursor.fetchone()['order_id']

                # 执行删除操作
                cursor.execute(sql, (order_id,))
                if cursor.rowcount == 0:
                    logger.error(f"order删除失败:order_id为{order_id}")
                else:
                    logger.info(f"order删除成功: {order_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"order删除失败: {e}")
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

                # 获取随机的 order_id
                cursor.execute("SELECT order_id FROM orders WHERE status = 'completed' ORDER BY RAND() LIMIT 1")
                order_id = cursor.fetchone()['order_id']

                # 生成随机数据
                fare = round(random.uniform(10, 100), 2)
                payment_method = random.choice(['credit_card', 'debit_card', 'cash'])
                status = random.choice(['pending', 'completed', 'failed'])
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

    @task(3)
    def update_payment(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 更新数据的 SQL 语句
                sql = "UPDATE `payments` SET `status` = %s WHERE `payment_id` = %s"

                # 生成随机的更新数据
                cursor.execute("SELECT payment_id, status FROM payments ORDER BY RAND() LIMIT 1")
                result_0 = cursor.fetchone() #此函数只能调用一次
                if result_0 is None:
                    print("没有payment数据")
                    return
                payment_id = result_0['payment_id']
                status = result_0['status']
                if status == 'pending':
                    status = random.choice(['completed', 'failed'])

                    # 执行更新操作
                    cursor.execute(sql, (status, payment_id))
                    if cursor.rowcount == 0:
                        logger.error(f"payment更新失败:数据库不存在payment_id为{payment_id}的数据")
                    else:
                        logger.info(f"payment更新成功: {status}, {payment_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"payment更新失败: {e}")
            self.db_conn.rollback()

    @task(1)
    def delete_payment(self):
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 删除数据的 SQL 语句
                sql = "DELETE FROM `payments` WHERE `payment_id` = %s"

                # 生成随机的删除数据
                cursor.execute("SELECT payment_id FROM payments ORDER BY RAND() LIMIT 1")
                payment_id = cursor.fetchone()['payment_id']

                # 执行删除操作
                cursor.execute(sql, (payment_id,))
                if cursor.rowcount == 0:
                    logger.error(f"payment删除失败:payment_id为{payment_id}")
                else:
                    logger.info(f"payment删除成功: {payment_id}")
            # 提交事务
            self.db_conn.commit()
        except MySQLError as e:
            logger.error(f"payment删除失败: {e}")
            self.db_conn.rollback()

