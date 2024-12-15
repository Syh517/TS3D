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
from requests.exceptions import HTTPError
from datetime import datetime
from urllib3.exceptions import NameResolutionError
from concurrent.futures import ThreadPoolExecutor, as_completed

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
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][info][{log}]\n")
                logger.info("数据库连接成功")
                return conn
            except MySQLError as e:
                now = datetime.now()
                log="数据库连接失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{e}]\n")
                logger.error(f"数据库连接失败: {e}")
                return None


    # @task()
    def call_api(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
            # 执行数据库更新测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:

                    # 调用外部API
                    response = requests.get("https://www.iqiyi.com/?vfm=f_588_wrb&fv=ac30238882b84c8c")
                    if response.status_code == 200:
                        now = datetime.now()
                        log="调用成功"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][info][{log}]\n")
                        logger.info(f"调用成功")
                    else:
                        now = datetime.now()
                        log="调用失败"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}]\n")
                        logger.error(f"调用失败")

                # 提交事务
                self.db_conn.commit()
            except MySQLError as e:
                now = datetime.now()
                log="调用失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{e}]\n")
                logger.error(f"调用失败: {e}")
                self.db_conn.rollback()


    # def call_api_0(self, task_id):
    #     with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
    #         try:
    #             response = requests.get("https://www.iqiyi.com/?vfm=f_588_wrb&fv=ac30238882b84c8c")
    #             # if response.status_code == 200:
    #             #     logger.info(f"调用成功")
    #             # else:
    #             #     now = datetime.now()
    #             #     log=f"Task {task_id}: 调用失败"
    #             #     file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}]\n")
    #             #     logger.error(f"Task {task_id}调用失败")
    #         except OSError as os_err:
    #             now = datetime.now()
    #             log=f"Task {task_id}: 调用失败"
    #             file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{os_err}]\n")
    #             logger.error(f"Task {task_id}调用失败: {os_err}")
    #         except HTTPError as http_err:
    #             now = datetime.now()
    #             log=f"Task {task_id}: 调用失败"
    #             file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{http_err}]\n")
    #             logger.error(f"Task {task_id}调用失败: {http_err}")
    #         except Exception as err:
    #             now = datetime.now()
    #             log=f"Task {task_id}: 调用失败"
    #             file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{err}]\n")
    #             logger.error(f"Task {task_id}调用失败: {err}")
    #         except NameResolutionError as err:
    #             now = datetime.now()
    #             log=f"Task {task_id}: 调用失败"
    #             file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{err}]\n")
    #             logger.error(f"Task {task_id}调用失败: {err}")
    #         except requests.exceptions.RequestException as err:
    #             now = datetime.now()
    #             log=f"Task {task_id}: 调用失败"
    #             file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{err}]\n")
    #             logger.error(f"Task {task_id}调用失败: {err}")


    def call_api_0(self, task_id):
        try:
            response = requests.get("https://www.iqiyi.com/?vfm=f_588_wrb&fv=ac30238882b84c8c")
            if response.status_code == 200:
                now = datetime.now()
                log=f"Task {task_id}: 调用成功"
                logger.info(f"调用成功")
                return f"[{now}][{self.node}][database_abnormal][abnormal_api][info][{log}]\n"
            else:
                now = datetime.now()
                log=f"Task {task_id}: 调用失败"
                logger.error(f"Task {task_id}调用失败")
                return f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}]\n"
        except OSError as os_err:
            now = datetime.now()
            log=f"Task {task_id}: 调用失败"
            logger.error(f"Task {task_id}调用失败: {os_err}")
            return f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{os_err}]\n"
        except HTTPError as http_err:
            now = datetime.now()
            log=f"Task {task_id}: 调用失败"
            logger.error(f"Task {task_id}调用失败: {http_err}")
            return f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{http_err}]\n"
        except Exception as err:
            now = datetime.now()
            log=f"Task {task_id}: 调用失败"
            logger.error(f"Task {task_id}调用失败: {err}")
            return f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{err}]\n"
        except NameResolutionError as err:
            now = datetime.now()
            log=f"Task {task_id}: 调用失败"
            logger.error(f"Task {task_id}调用失败: {err}")
            return f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{err}]\n"
        except requests.exceptions.RequestException as err:
            now = datetime.now()
            log=f"Task {task_id}: 调用失败"
            logger.error(f"Task {task_id}调用失败: {err}")
            return f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{err}]\n"
        


    @task()
    def parallel_api_calls(self):
        with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
            # 执行数据库更新测试逻辑
            if self.db_conn is None:
                now = datetime.now()
                log="数据库连接未初始化"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}]\n")
                logger.error("数据库连接未初始化")
                return

            try:
                with self.db_conn.cursor() as cursor:
                    try:
                        with ThreadPoolExecutor(max_workers=100) as executor:
                            # 使用列表推导式生成多个并行任务
                            futures = [executor.submit(self.call_api_0, i) for i in range(90)]

                            results = []
                            for future in as_completed(futures):
                                result = future.result()
                                if result:
                                    results.append(result)
                                    file.write(result)
                    except OSError as os_err:
                        now = datetime.now()
                        log="调用失败"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{os_err}]\n")
                        logger.error(f"OSError: {os_err}")
                    except Exception as err:
                        now = datetime.now()
                        log="调用失败"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{err}]\n")
                        logger.error(f"调用失败: {err}")
            except OSError as os_err:
                        now = datetime.now()
                        log="调用失败"
                        file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{os_err}]\n")
                        logger.error(f"OSError: {os_err}")
            except MySQLError as e:
                now = datetime.now()
                log="调用失败"
                file.write(f"[{now}][{self.node}][database_abnormal][abnormal_api][error][{log}][{e}]\n")
                logger.error(f"调用失败: {e}")



