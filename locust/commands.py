import subprocess

def run_kubectl_command_1(command):
    try:
        # 使用 subprocess.run 执行命令，并捕获输出
        result = subprocess.run(command, capture_output=False, text=True, check=True)
        print("Locust 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，捕获异常并返回错误信息
        print(f"Locust 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"
    
def run_kubectl_command_2(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True, check=True)
        print("Locust 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Locust 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"



# 定义要执行的 locust 命令
locust_command_1 = [
    "locust",
    "-f", "normal_all.py",          # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

locust_command_2 = [
    "locust",
    "-f", "normal_select.py",       # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

locust_command_3 = [
    "locust",
    "-f", "normal_insert.py",       # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

locust_command_4 = [
    "locust",
    "-f", "test.py",                # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

locust_command_5 = [
    "locust",
    "-f", "abnormal_insert.py",     # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

#复杂查询；全表扫描
locust_command_6 = [
    "locust",
    "-f", "abnormal_select_1.py",     # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

#聚合查询
locust_command_7 = [
    "locust",
    "-f", "abnormal_select_2.py",     # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

locust_command_8 = [
    "locust",
    "-f", "abnormal_api.py",     # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

locust_command_9 = [
    "locust",
    "-f", "abnormal_deadlock.py",     # 指定 Locust 文件
    "--headless",                   # 无头模式（不打开浏览器）
    "-u", "100",                    # 用户数
    "-r", "10",                     # 每秒启动的用户数
    "-t", "10s"                     # 运行时间
]

locust_command_0="locust -f test.py --headless -u 100 -r 10 -t 10s"
# output1 = run_kubectl_command_1(locust_command_4)
output2 = run_kubectl_command_2(locust_command_0)


