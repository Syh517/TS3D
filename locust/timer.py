from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# 定义正常时段执行的函数
def normal_function():
    print(f"Normal function executed at {datetime.now()}")

# 定义异常时段执行的函数
def exception_function_morning():
    print(f"Morning exception function executed at {datetime.now()}")

def exception_function_afternoon():
    print(f"Afternoon exception function executed at {datetime.now()}")

def exception_function_evening():
    print(f"Evening exception function executed at {datetime.now()}")

# 创建后台调度器
scheduler = BackgroundScheduler()

# 添加正常时段任务，例如每天的08:00-10:00和12:00-14:00和17:00-19:00
scheduler.add_job(normal_function, 'cron', hour='8-10,12,14-17,19-20', minute='*/2')  # 每2分钟执行一次

# 添加异常时段任务
# 10-12点的异常任务
for hour in range(10, 13):
        scheduler.add_job(exception_function_morning, 'cron', hour=hour, minute='*/2')

# 14-17点的异常任务
for hour in range(14, 18):
        scheduler.add_job(exception_function_afternoon, 'cron', hour=hour, minute='*/2')

# 19-21点的异常任务
for hour in range(19, 22):
        scheduler.add_job(exception_function_evening, 'cron', hour=hour, minute='*/2')

# 启动调度器
scheduler.start()

# 主程序继续执行其他任务
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()