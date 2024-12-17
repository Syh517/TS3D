from kubernetes import client, config
import pymysql

# 加载 Kubernetes 配置
config.load_kube_config()


# 获取 MySQL Pod 的 IP 地址


# MySQL 连接配置
config = {
    "host": "172.18.0.2",  # Node 的 IP 地址
    "port": 32440,    # 暴露的服务的端口
    "user": "root",  # MySQL 用户名
    "password": "",  # MySQL 密码（如果设置了密码）
    "database": "taxi",  # 数据库名称
    "charset": "utf8mb4",  # 字符集
}

try:
    # 连接到 MySQL
    connection = pymysql.connect(**config)
    print("连接成功")

    # 执行查询
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print(f"MySQL 版本: {result[0]}")

finally:
    # 关闭连接
    connection.close()