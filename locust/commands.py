import subprocess

def run_command_1(command):
    try:
        # 使用 subprocess.run 执行命令，并捕获输出
        result = subprocess.run(command, capture_output=False, text=True, check=True)
        print("Locust 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，捕获异常并返回错误信息
        print(f"Locust 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"
    
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True, check=True)
        print("Locust 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Locust 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"



# 定义要执行的 locust 命令
normal_all_commond="locust -f normal_all.py --headless -u 100 -r 10 -t 60s"
normal_select_commond="locust -f normal_select.py --headless -u 100 -r 10 -t 60s"
abnormal_insert_commond="locust -f abnormal_insert.py --headless -u 100 -r 10 -t 120s"
abnormal_select_1_commond="locust -f abnormal_select_1.py --headless -u 100 -r 100 -t 120s"
abnormal_select_2_commond="locust -f abnormal_select_2.py --headless -u 100 -r 100 -t 120s"
abnormal_select_pod_commond="locust -f abnormal_select_pod_6.py --headless -u 100 -r 100 -t 120s"
abnormal_api_commond="locust -f abnormal_api.py --headless -u 1000 -r 1000 -t 10s"
abnormal_deadlock_commond="locust -f abnormal_deadlock.py --headless -u 100 -r 10 -t 120s"
abnormal_frequency_commond="locust -f abnormal_frequency.py --headless -u 10000 -r 1000 -t 60s"

locust_command_0="locust -f test.py --headless -u 100 -r 10 -t 10s"


def init():
    mysql_0_connect="kubectl port-forward pod/mysql-0 3306:3306 &"
    run_command(mysql_0_connect)

    mysql_1_connect="kubectl port-forward pod/mysql-1 3307:3306 &"
    run_command(mysql_1_connect)

    mysql_2_connect="kubectl port-forward pod/mysql-2 3308:3306 &"
    run_command(mysql_2_connect)

    mysql_3_connect="kubectl port-forward pod/mysql-3 3309:3306 &"
    run_command(mysql_3_connect)

    mysql_4_connect="kubectl port-forward pod/mysql-4 3305:3306 &"
    run_command(mysql_4_connect)

    mysql_5_connect="kubectl port-forward pod/mysql-5 3304:3306 &"
    run_command(mysql_5_connect)

    mysql_6_connect="kubectl port-forward pod/mysql-6 3303:3306 &"
    run_command(mysql_6_connect)


if __name__ == "__main__":
    # init()
    run_command(abnormal_frequency_commond)


