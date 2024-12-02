import mysql.connector
from mysql.connector import Error

# 配置数据库连接参数
config = {
    # 'host': '172.20.0.2',  # MySQL Node的IP地址
    # 'port': '30007',       # NodePort

    'host': '127.0.0.1',  # MySQL Pod的IP地址
    'port': '3306',       # Port

    'user': 'root',        # MySQL用户名 
    'password': '',        # MySQL密码
    'database': 'first'    # 要操作的数据库名称
}
# 创建连接
connection = mysql.connector.connect(**config)
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("成功连接到 MySQL 数据库，版本：", db_Info)
    # 创建游标对象
    cursor = connection.cursor()

    # 编写SQL语句
    sql = "CREATE TABLE IF NOT EXISTS u (\
        id INT AUTO_INCREMENT PRIMARY KEY,\
        username VARCHAR(50) NOT NULL\
    );"


    # 执行SQL语句
    cursor.execute(sql)
    
    # 提交事务
    connection.commit()
    print("执行成功")
    
    # 关闭游标和连接
    cursor.close()
    connection.close()
    print("MySQL 连接已关闭")



# # 尝试创建数据库连接
# try:
#     # 创建连接
#     connection = mysql.connector.connect(**config)
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("成功连接到 MySQL 数据库，版本：", db_Info)
#         # 创建游标对象
#         cursor = connection.cursor()

#         # 编写SQL语句
#         sql = "CREATE TABLE IF NOT EXISTS users (\
#             id INT AUTO_INCREMENT PRIMARY KEY,\
#             username VARCHAR(50) NOT NULL\
#         );"

#         # 执行SQL语句
#         cursor.execute(sql)
        
#         # 提交事务
#         connection.commit()
#         print("执行成功")
        
#         # 关闭游标和连接
#         cursor.close()
#         connection.close()
#         print("MySQL 连接已关闭")
         
# except Error as e:
#     print("连接错误：", e)
