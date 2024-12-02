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
    def select_drivers(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `drivers`"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"driver数据查询成功")
                else:
                    logger.info("未查询到driver数据")
        except MySQLError as e:
            logger.error(f"driver数据查询失败: {e}")


    @task
    def select_users(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `users`"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"user数据查询成功")
                else:
                    logger.info("未查询到user数据")
        except MySQLError as e:
            logger.error(f"user数据查询失败: {e}")

    
    @task
    def select_orders(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `orders`"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"order数据查询成功")
                else:
                    logger.info("未查询到order数据")
                
        except MySQLError as e:
            logger.error(f"order数据查询失败: {e}")

    @task
    def select_payments(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql = "SELECT * FROM `payments`"
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"payment数据查询成功")
                else:
                    logger.info("未查询到payment数据")
        except MySQLError as e:
            logger.error(f"payment数据查询失败: {e}")

    #大表关联查询：查询所有已完成订单的详细信息，包括用户名、司机名、订单状态和支付状态
    @task
    def select_1(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT
                            u.name AS user_name,
                            d.name AS driver_name,
                            o.status AS order_status,
                            p.status AS payment_status
                        FROM 
                            orders o
                        JOIN 
                            users u ON o.user_id = u.user_id
                        JOIN 
                            drivers d ON o.driver_id = d.driver_id
                        JOIN 
                            payments p ON o.order_id = p.order_id
                        WHERE 
                            o.status = 'completed';'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"select_1数据查询成功")
                else:
                    logger.info("未查询到select_1数据")
        except MySQLError as e:
            logger.error(f"select_1数据查询失败: {e}")


    #子查询：查询所有支付失败的订单，并显示订单的详细信息，包括用户名、司机名、订单状态和支付状态
    @task
    def select_2(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT 
                            u.name AS user_name,
                            d.name AS driver_name,
                            o.status AS order_status,
                            p.status AS payment_status
                        FROM 
                            orders o
                        JOIN 
                            users u ON o.user_id = u.user_id
                        JOIN 
                            drivers d ON o.driver_id = d.driver_id
                        JOIN 
                            payments p ON o.order_id = p.order_id
                        WHERE 
                            p.status = 'failed';'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"select_2数据查询成功")
                else:
                    logger.info("未查询到select_2数据")
        except MySQLError as e:
            logger.error(f"select_2数据查询失败: {e}")

    
    #多表连接查询：查询所有用户的订单历史，包括用户名、订单ID、司机名、订单状态和支付状态
    @task
    def select_3(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT 
                            u.name AS user_name,
                            o.order_id,
                            d.name AS driver_name,
                            o.status AS order_status,
                            p.status AS payment_status
                        FROM 
                            users u
                        LEFT JOIN 
                            orders o ON u.user_id = o.user_id
                        LEFT JOIN 
                            drivers d ON o.driver_id = d.driver_id
                        LEFT JOIN 
                            payments p ON o.order_id = p.order_id
                        ORDER BY 
                            u.user_id, o.order_id;'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"select_3数据查询成功")
                else:
                    logger.info("未查询到select_3数据")
        except MySQLError as e:
            logger.error(f"select_3数据查询失败: {e}")


    #嵌套查询：查询所有订单金额大于平均订单金额的订单，并显示订单的详细信息，包括用户名、司机名、订单状态和支付状态
    @task
    def select_4(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT 
                            u.name AS user_name,
                            d.name AS driver_name,
                            o.status AS order_status,
                            p.status AS payment_status
                        FROM 
                            orders o
                        JOIN 
                            users u ON o.user_id = u.user_id
                        JOIN 
                            drivers d ON o.driver_id = d.driver_id
                        JOIN 
                            payments p ON o.order_id = p.order_id
                        WHERE 
                            p.fare > (SELECT AVG(fare) FROM payments);'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"select_4数据查询成功")
                else:
                    logger.info("未查询到select_4数据")
        except MySQLError as e:
            logger.error(f"select_4数据查询失败: {e}")


    #复杂嵌套查询：查询所有用户中，至少有一个订单支付失败的用户的详细信息，包括用户名、电话和邮箱
    @task
    def select_5(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT 
                            u.name,
                            u.phone,
                            u.email
                        FROM 
                            users u
                        WHERE 
                            EXISTS (
                                SELECT 1
                                FROM 
                                    orders o
                                JOIN 
                                    payments p ON o.order_id = p.order_id
                                WHERE 
                                    o.user_id = u.user_id
                                    AND p.status = 'failed'
                            );'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"select_5数据查询成功")
                else:
                    logger.info("未查询到select_5数据")
        except MySQLError as e:
            logger.error(f"select_5数据查询失败: {e}")


    #多表连接与子查询结合：查询所有司机中，至少有一个订单金额大于100的司机的详细信息，包括司机名、电话和驾照号码
    @task
    def select_6(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT 
                            d.name,
                            d.phone,
                            d.license_number
                        FROM 
                            drivers d
                        WHERE 
                            EXISTS (
                                SELECT 1
                                FROM 
                                    orders o
                                JOIN 
                                    payments p ON o.order_id = p.order_id
                                WHERE 
                                    o.driver_id = d.driver_id
                                    AND p.fare > 100
                            );'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"select_6数据查询成功")
                else:
                    logger.info("未查询到select_6数据")
        except MySQLError as e:
            logger.error(f"select_6数据查询失败: {e}")


    #复杂条件查询：查询所有订单中，用户和司机的姓名都包含特定字符串的订单详细信息
    @task
    def select_7(self):
        # 执行数据库查询测试逻辑
        if self.db_conn is None:
            logger.error("数据库连接未初始化")
            return

        try:
            with self.db_conn.cursor() as cursor:
                # 查询数据的 SQL 语句
                sql ='''SELECT 
                            u.name AS user_name,
                            d.name AS driver_name,
                            o.status AS order_status,
                            p.status AS payment_status
                        FROM 
                            orders o
                        JOIN 
                            users u ON o.user_id = u.user_id
                        JOIN 
                            drivers d ON o.driver_id = d.driver_id
                        JOIN 
                            payments p ON o.order_id = p.order_id
                        WHERE 
                            u.name LIKE '%John%'
                            AND d.name LIKE '%John%';'''
                # 执行查询操作
                cursor.execute(sql)
                result = cursor.fetchall()
                if result:
                    logger.info(f"select_7数据查询成功")
                else:
                    logger.info("未查询到select_7数据")
        except MySQLError as e:
            logger.error(f"select_7数据查询失败: {e}")

