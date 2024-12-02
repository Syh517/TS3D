import schedule
import time
import random
import threading
from datetime import datetime, time as dt_time


def job1():
    print("I'm working for job1 start", datetime.datetime.now())
    time.sleep(5)
    print("job1: end", datetime.datetime.now())

def job2():
    print("I'm working for job2 start", datetime.datetime.now())
    time.sleep(4)
    print("job2: end", datetime.datetime.now())

def job3():
    print("I'm working for job3 start", datetime.datetime.now())
    time.sleep(3)
    print("job3: end", datetime.datetime.now())


# 定义一些异常函数
def exception_function1():
    threading.Thread(target=job1).start()

def exception_function2():
    threading.Thread(target=job2).start()

def exception_function3():
    threading.Thread(target=job3).start()

# 存储所有异常函数的列表
exception_functions = [
    exception_function1,
    exception_function2,
    exception_function3
]

jobs = []
def schedule_random_exception_functions():
    now = datetime.now()
    current_minute = now.minute
    current_second = now.second
    print(current_second)
    
    # 随机选择一个秒数，确保它在当前分钟的剩余秒数内
    second = random.randint(current_second+1, 59)
    time_str = f":{second:02d}"
    
    print(f"将在当前分钟的第 {second} 秒执行任务")
    now2 = datetime.now()
    current_second2 = now2.second
    print(current_second2)
    
    chosen_function = random.choice(exception_functions)
    print(chosen_function)

    # 如果已经有一个job在运行，取消它
    if jobs:
        for job in jobs:
            schedule.cancel_job(job)
        jobs=[]
    

    job = schedule.every().minute.at(time_str).do(chosen_function)
    jobs.append(job)
    print(jobs)


schedule.every().minute.do(schedule_random_exception_functions)











jobs = []
def execute_random_functions():
    target_times=[]
    times=[]
    # 随机选择执行次数，例如在1到3次之间
    num_executions = random.randint(2, 4)
    print(num_executions)
    current_time = datetime.now()


    for _ in range(num_executions):
        hour = random.randint(10, 11)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        # 构建完整的时间字符串
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        # 计算目标时间
        target_time = current_time.replace(hour=hour, minute=minute, second=second, microsecond=0)
        target_times.append(target_time)
        times.append(time_str)
    
    target_times.sort()
    times=sorted(times, key=lambda x: datetime.strptime(x, "%H:%M:%S"))
    print(target_times)
    print(times)

    
    for i in range(num_executions):
        # 随机选择一个异常函数
        chosen_function = random.choice(exception_functions)
        
        # 安排随机选择的异常函数在随机时间执行
        job = schedule.every().day.at(times[i]).do(chosen_function)
        jobs.append(job)
        
def clear_jobs():
    for job in jobs:
        schedule.cancel_job(job)
    jobs=[]            

# # 安排任务，每天10点到12点之间执行随机次数的随机异常函数
# schedule.every().day.at("10:00").do(execute_random_functions)
# schedule.every().day.at("12:00").do(clear_jobs)

# schedule.every(10).seconds.do(execute_random_functions)

# 持续运行调度器
while True:
    schedule.run_pending()
    time.sleep(1)



