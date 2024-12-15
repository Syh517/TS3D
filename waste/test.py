from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import subprocess
import random
import time
import os



# 执行命令
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.stderr}"



# 正常
normal_all_commond="locust -f locust/normal_all.py --headless -u 100 -r 10 -t 60s"
normal_select_commond="locust -f locust/normal_select.py --headless -u 100 -r 10 -t 60s"

def normal_all():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="normal_all"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[normal_all][{begin_time}][{function_name}]\n")
        run_command(normal_all_commond)

def normal_select():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="normal_select"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[normal_select][{begin_time}][{function_name}]\n")
        run_command(normal_select_commond)



# 数据库异常
abnormal_insert_commond="locust -f /home/yyy/mysql/locust/abnormal_insert.py --headless -u 100 -r 10 -t 10s"
abnormal_select_1_commond="locust -f /home/yyy/mysql/locust/abnormal_select_1.py --headless -u 100 -r 100 -t 10s"
abnormal_select_2_commond="locust -f /home/yyy/mysql/locust/abnormal_select_2.py --headless -u 100 -r 100 -t 10s"
abnormal_api_commond="locust -f /home/yyy/mysql/locust/abnormal_api.py --headless -u 100 -r 100 -t 10s"
abnormal_deadlock_commond="locust -f /home/yyy/mysql/locust/abnormal_deadlock.py --headless -u 100 -r 10 -t 10s"
abnormal_frequency_commond="locust -f /home/yyy/mysql/locust/abnormal_frequency.py --headless -u 10000 -r 100 -t 10s"

abnormal_select_pod_1_commond="locust -f /home/yyy/mysql/locust/abnormal_select_pod_1.py --headless -u 100 -r 100 -t 10s"
abnormal_select_pod_2_commond="locust -f /home/yyy/mysql/locust/abnormal_select_pod_2.py --headless -u 100 -r 100 -t 10s"
abnormal_select_pod_3_commond="locust -f /home/yyy/mysql/locust/abnormal_select_pod_3.py --headless -u 100 -r 100 -t 10s"
abnormal_select_pod_4_commond="locust -f /home/yyy/mysql/locust/abnormal_select_pod_4.py --headless -u 100 -r 100 -t 10s"
abnormal_select_pod_5_commond="locust -f /home/yyy/mysql/locust/abnormal_select_pod_5.py --headless -u 100 -r 100 -t 10s"
abnormal_select_pod_6_commond="locust -f /home/yyy/mysql/locust/abnormal_select_pod_6.py --headless -u 100 -r 100 -t 10s"

def abnormal_insert():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_insert"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_insert_commond)

def abnormal_select_1():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_1"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_1_commond)

def abnormal_select_2():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_2"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_2_commond)

def abnormal_api():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_api"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_api_commond)

def abnormal_deadlock():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_deadlock"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_deadlock_commond)

def abnormal_frequency():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_frequency"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_frequency_commond)

def abnormal_select_pod_1():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_pod"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        time.sleep(2)
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_pod_1_commond)


def abnormal_select_pod_2():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_pod"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        time.sleep(2)
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_pod_2_commond)


def abnormal_select_pod_3():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_pod"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        time.sleep(2)
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_pod_3_commond)


def abnormal_select_pod_4():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_pod"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        time.sleep(2)
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_pod_4_commond)


def abnormal_select_pod_5():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_pod"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        time.sleep(2)
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_pod_5_commond)

def abnormal_select_pod_6():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="abnormal_select_pod"
        print(f"{function_name} executed at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        time.sleep(2)
        file.write(f"[database_abnormal][{begin_time}][{function_name}]\n")
        run_command(abnormal_select_pod_6_commond)




database_abnormal_1 = [
    abnormal_insert,
    abnormal_select_1,
    abnormal_select_2,
    abnormal_api,
    abnormal_deadlock,
    abnormal_frequency
    ]

database_abnormal_selects = [
    abnormal_select_pod_1,
    abnormal_select_pod_2,
    abnormal_select_pod_3,
    abnormal_select_pod_4,
    abnormal_select_pod_5,
    abnormal_select_pod_6
    ]



# 系统异常
# network_delay_start="kubectl annotate networkchaos network-delay experiment.chaos-mesh.org/pause- --overwrite"
# network_delay_stop="kubectl annotate networkchaos network-delay experiment.chaos-mesh.org/pause=true --overwrite"

# memory_stress_start="kubectl annotate stresschaos memory-stress experiment.chaos-mesh.org/pause- --overwrite"
# memory_stress_stop="kubectl annotate stresschaos memory-stress experiment.chaos-mesh.org/pause=true --overwrite"

# cpu_stress_start="kubectl annotate stresschaos cpu-stress experiment.chaos-mesh.org/pause- --overwrite"
# cpu_stress_stop="kubectl annotate stresschaos cpu-stress experiment.chaos-mesh.org/pause=true --overwrite"

# io_stress_start="kubectl annotate iochaos io-stress experiment.chaos-mesh.org/pause- --overwrite"
# io_stress_stop="kubectl annotate iochaos io-stress experiment.chaos-mesh.org/pause=true --overwrite"

# network_partition_start="kubectl annotate networkchaos network-partition experiment.chaos-mesh.org/pause- --overwrite"
# network_partition_stop="kubectl annotate networkchaos network-partition experiment.chaos-mesh.org/pause=true --overwrite"

# pod_failure_start="kubectl annotate podchaos pod-failure experiment.chaos-mesh.org/pause- --overwrite"
# pod_failure_stop="kubectl annotate podchaos pod-failure experiment.chaos-mesh.org/pause=true --overwrite"


network_delay_start="kubectl apply -f chaos/network-delay.yaml"
network_delay_stop="kubectl delete -f chaos/network-delay.yaml"

memory_stress_start="kubectl apply -f chaos/memory-stress.yaml"
memory_stress_stop="kubectl delete -f chaos/memory-stress.yaml"

cpu_stress_start="kubectl apply -f chaos/cpu-stress.yaml"
cpu_stress_stop="kubectl delete -f chaos/cpu-stress.yaml"

io_stress_start="kubectl apply -f chaos/io-stress.yaml"
io_stress_stop="kubectl delete -f chaos/io-stress.yaml"

network_partition_start="kubectl apply -f chaos/network-partition.yaml"
network_partition_stop="kubectl delete -f chaos/network-partition.yaml"

pod_failure_start="kubectl apply -f chaos/pod-failure.yaml"
pod_failure_stop="kubectl delete -f chaos/pod-failure.yaml"

def network_delay():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="network_delay"
        print(f"{function_name} start at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        run_command(network_delay_start)
        time.sleep(360)  # 暂停6分钟
        print(f"{function_name} stop at {datetime.datetime.now()}")
        run_command(network_delay_stop)
        end_time=datetime.datetime.now()
        file.write(f"[system_abnormal][{begin_time}][{end_time}][{function_name}]\n")

def memory_stress():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="memory_stress"
        print(f"{function_name} start at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        run_command(memory_stress_start)
        time.sleep(360)  
        print(f"{function_name} stop at {datetime.datetime.now()}")
        run_command(memory_stress_stop)
        end_time=datetime.datetime.now()
        file.write(f"[system_abnormal][{begin_time}][{end_time}][{function_name}]\n")

def cpu_stress():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="cpu_stress"
        print(f"{function_name} start at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        run_command(cpu_stress_start)
        time.sleep(360)  
        print(f"{function_name} stop at {datetime.datetime.now()}")
        run_command(cpu_stress_stop)
        end_time=datetime.datetime.now()
        file.write(f"[system_abnormal][{begin_time}][{end_time}][{function_name}]\n")

def io_stress():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="io_stress"
        print(f"{function_name} start at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        run_command(io_stress_start)
        time.sleep(360)  
        print(f"{function_name} stop at {datetime.datetime.now()}")
        run_command(io_stress_stop)
        end_time=datetime.datetime.now()
        file.write(f"[system_abnormal][{begin_time}][{end_time}][{function_name}]\n")

def network_partition():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="network_partition"
        print(f"{function_name} start at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        run_command(network_partition_start)
        time.sleep(360)  
        print(f"{function_name} stop at {datetime.datetime.now()}")
        run_command(network_partition_stop)
        end_time=datetime.datetime.now()
        file.write(f"[system_abnormal][{begin_time}][{end_time}][{function_name}]\n")

def pod_failure():
    with open("/home/yyy/mysql/data/logs/logs.txt",'a') as file:
        function_name="pod_failure"
        print(f"{function_name} start at {datetime.datetime.now()}")
        begin_time=datetime.datetime.now()
        run_command(pod_failure_start)
        time.sleep(360)  
        print(f"{function_name} stop at {datetime.datetime.now()}")
        run_command(pod_failure_stop)
        end_time=datetime.datetime.now()
        file.write(f"[system_abnormal][{begin_time}][{end_time}][{function_name}]\n")


system_abnormal = [
    network_delay,
    memory_stress,
    cpu_stress,
    io_stress,
    network_partition,
    pod_failure
    ]



# 使用集合来记录已执行过的函数，集合可以保证元素唯一性
executed_database_abnormal = set()
executed_system_abnormal = set()  
executed_database_abnormal_selects = set()

def random_database_abnormal():
    chosen_function = random.choice(database_abnormal_1)
    if len(executed_database_abnormal) < len(database_abnormal_1):
        while chosen_function in executed_database_abnormal:
            chosen_function = random.choice(database_abnormal_1)
        executed_database_abnormal.add(chosen_function)
    return chosen_function    
def random_system_abnormal():
    chosen_function = random.choice(system_abnormal)
    if len(executed_system_abnormal) < len(system_abnormal):
        while chosen_function in executed_system_abnormal:
            chosen_function = random.choice(system_abnormal)
        executed_system_abnormal.add(chosen_function)
    return chosen_function    


def execute_database_abnormal():
    chosen_function = random_database_abnormal()
    chosen_function()

def execute_system_abnormal():
    chosen_function = random_system_abnormal()
    chosen_function()



def execute_database_abnormal_selects_1():
    executed_database_abnormal_selects.clear()
    chosen_function = random.choice(database_abnormal_selects)
    executed_database_abnormal_selects.add(chosen_function)
    chosen_function()

def execute_database_abnormal_selects_2():
    chosen_function = random.choice(database_abnormal_selects)
    while chosen_function in executed_database_abnormal_selects:
        chosen_function = random.choice(database_abnormal_selects)

    executed_database_abnormal_selects.add(chosen_function)
    chosen_function()





# 清空所有执行列表、停止所有系统异常、转发mysql pod端口
def init():
    executed_database_abnormal.clear()
    executed_database_abnormal_selects.clear()
    executed_system_abnormal.clear()

    # run_command(network_delay_stop)
    # run_command(memory_stress_stop)
    # run_command(cpu_stress_stop)
    # run_command(io_stress_stop)
    # run_command(network_partition_stop)
    # run_command(pod_failure_stop)

    if not os.path.exists("/home/yyy/mysql/data/logs"):
        os.makedirs("/home/yyy/mysql/data/logs")

    with open("/home/yyy/mysql/data/logs/logs.txt",'w') as file:
        pass

    with open("/home/yyy/mysql/data/logs/sqls.txt",'w') as file2:
        pass

    mysql_0_connect="kubectl port-forward pod/mysql-0 3306:3306 &"
    run_command(mysql_0_connect)

    mysql_1_connect="kubectl port-forward pod/mysql-1 3307:3306 &"
    run_command(mysql_1_connect)

    mysql_2_connect="kubectl port-forward pod/mysql-1 3308:3306 &"
    run_command(mysql_2_connect)

    mysql_3_connect="kubectl port-forward pod/mysql-1 3309:3306 &"
    run_command(mysql_3_connect)

    mysql_4_connect="kubectl port-forward pod/mysql-1 3305:3306 &"
    run_command(mysql_4_connect)

    mysql_5_connect="kubectl port-forward pod/mysql-1 3304:3306 &"
    run_command(mysql_5_connect)

    mysql_6_connect="kubectl port-forward pod/mysql-1 3303:3306 &"
    run_command(mysql_6_connect)

    


# 创建后台调度器
scheduler = BackgroundScheduler()


# 添加任务，设置定时器
def add_jobs():
    # 移除之前添加过的所有任务，避免重复添加（如果有需要重新配置任务的情况）
    scheduler.remove_all_jobs()

    scheduler.add_job(abnormal_select_1, 'cron', second='*/30')
    scheduler.add_job(abnormal_select_pod_3, 'cron', second='*/30')

    # 添加任务，在其他时间执行正常函数

    # scheduler.add_job(normal_all, 'cron', minute='*/5')
    # scheduler.add_job(normal_select, 'cron', minute='*/5')

def execute():

    add_jobs()

    # 获取当前时间和结束时间
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(days=7)

    scheduler.start()
    try:
        # 保持主程序运行，让调度器可以在后台持续工作
        while datetime.datetime.now() < end_time:
            pass
    except (KeyboardInterrupt, SystemExit):
        # 当接收到中断信号（如Ctrl+C）时，关闭调度器
        scheduler.shutdown()


if __name__ == "__main__":
    pkill_commond = "pkill -f kubectl"
    run_command(pkill_commond)


    init()

    execute()





