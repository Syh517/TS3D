from kubernetes import client, config
import time
import requests
import os
import subprocess
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector

# 加载 kubeconfig 配置
config.load_kube_config()

# 指定命名空间
namespace = 'default'

# Prometheus 的 URL
prometheus_url = "http://localhost:9091/api/v1/query"

config = {
    'host': '172.18.0.2',  # MySQL Node的IP地址
    'port': '30007',       # NodePort
    'user': 'root',        # MySQL用户名 
    'password': '',        # MySQL密码
    'database': 'taxi',    # 要操作的数据库名称
}
connection = None
cursor = None

# 编写SQL语句
sql = "select concat(round(sum(data_length),2)) as data from information_schema.tables;"


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.stderr}"



# 使用 kubectl top pod 获取 Pod 的资源指标
def get_pod_metrics():
    try:
        result = subprocess.run(['kubectl', 'top', 'pod', '--no-headers'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting metrics: {e}")
        return None
#解析指标
def parse_kubectl_top_output(data):
    metrics = []
    for line in data.strip().split("\n"):
        # 分割行，按空格分隔
        columns = line.split()
        if len(columns) >= 3:
            pod_name = columns[0]
            if pod_name.startswith("sysbench-pod"):
                continue
            cpu_usage = columns[1].replace("m", "")  # 去掉 'm'
            memory_usage = columns[2].replace("Mi", "")  # 去掉 'Mi'
            metrics.append({
                "pod_name": pod_name,
                "cpu": int(cpu_usage),  # 转为整数
                "memory": int(memory_usage),  # 转为整数
            })
    return metrics



def mysql_metircs(query):
    response = requests.get(prometheus_url, params={'query': query})
    if response.status_code == 200:
        metrics = response.json()
        if metrics['status'] == 'success':
            results = metrics['data']['result']
            return results
        else:
            print(f"Query failed: {metrics['status']}")
            return "Error!"
    else:
        print(f"Failed to fetch metrics: {response.status_code}")
        return "Error!"

def handle_results(results):
    dict={}
    for result in results:
        instance = result['metric']['instance']
        dict[instance]=result['value'][1]
    
    return dict
        

abnormal_hours = ['10','11','14','15','16','19','20']
abnormal_hours_1 = ['10','11','19','20']
abnormal_hours_2 = ['14','15','16']

pod_names=["mysql-0","mysql-1","mysql-2","mysql-3","mysql-4","mysql-5","mysql-6"]



def job():
    print("Collecting...")
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
    except:
        timestamp=datetime.datetime.now()
        for pod_name in pod_names:
            print(pod_name)
            with open("/home/yyy/mysql/data/metrics/"+pod_name+"_metrics.txt",'a') as file1:
                # 获取并写入pod的指标数据
                # file1.write("指标:\n")
                file1.write(f"{timestamp},pod_unconnect,1\n")
        return

    cursor.execute(sql)
    disk_usage = cursor.fetchall()[0][0]
    
    #获取mysql指标数据
    q1 = 'rate(mysql_global_status_questions[1m])'
    # q2 = 'mysql_global_status_innodb_buffer_pool_pages_data' 
    q3 = 'mysql_global_status_innodb_buffer_pool_bytes_data'
    q4='rate(mysql_global_status_innodb_data_reads[1m]) + rate(mysql_global_status_innodb_data_writes[1m])'

    # 查询性能指标
    q5="rate(mysql_global_status_slow_queries[1m])"
    q6="rate(mysql_global_status_select_full_join[1m])"
    q7="rate(mysql_global_status_select_scan[1m])"

    # 连接和线程指标
    q8="rate(mysql_global_status_threads_created[1m])"
    q9="rate(mysql_global_status_aborted_connects[1m])"
    q10="rate(mysql_global_status_aborted_clients[1m])"

    # 缓存和内存使用指标
    "rate(mysql_global_status_buffer_pool_read_requests[1m])"
    "rate(mysql_global_status_buffer_pool_reads[1m])"
    "rate(mysql_global_status_buffer_pool_write_requests[1m])"

    # 锁和事务指标
    q11="rate(mysql_global_status_table_locks_waited[1m])"
    q12="rate(mysql_global_status_innodb_row_lock_waits[1m])"
    "rate(mysql_global_status_innodb_deadlocks[1m])"

    # InnoDB 存储引擎指标
    q13="rate(mysql_global_status_innodb_buffer_pool_read_requests[1m])"
    q14="rate(mysql_global_status_innodb_buffer_pool_reads[1m])"
    q15="rate(mysql_global_status_innodb_buffer_pool_write_requests[1m])"

    # 复制和主从同步指标
    q16="rate(mysql_slave_status_seconds_behind_master[1m])"

    # 全局状态指标
    q17="rate(mysql_global_status_connections[1m])"
    q18="rate(mysql_global_status_max_used_connections[1m])"

    # 查询缓存指标
    q19="rate(mysql_global_status_qcache_hits[1m])"
    q20="rate(mysql_global_status_qcache_inserts[1m])"
    q21="rate(mysql_global_status_qcache_lowmem_prunes[1m])"

    # 临时表指标
    q22="rate(mysql_global_status_created_tmp_tables[1m])"
    q23="rate(mysql_global_status_created_tmp_disk_tables[1m])"

    # 二进制日志指标
    q24="rate(mysql_global_status_binlog_cache_disk_use[1m])"
    q25="rate(mysql_global_status_binlog_cache_use[1m])"



    results1=mysql_metircs(q1)
    # results2=mysql_metircs(q2)
    results3=mysql_metircs(q3)
    results4=mysql_metircs(q4)
    results5=mysql_metircs(q5)
    results6=mysql_metircs(q6)
    results7=mysql_metircs(q7)
    results8=mysql_metircs(q8)
    results9=mysql_metircs(q9)
    results10=mysql_metircs(q10)
    results11=mysql_metircs(q11)
    results12=mysql_metircs(q12)
    results13=mysql_metircs(q13)
    results14=mysql_metircs(q14)
    results15=mysql_metircs(q15)
    results16=mysql_metircs(q16)
    results17=mysql_metircs(q17)
    results18=mysql_metircs(q18)
    results19=mysql_metircs(q19)
    results20=mysql_metircs(q20)
    results21=mysql_metircs(q21)
    results22=mysql_metircs(q22)
    results23=mysql_metircs(q23)
    results24=mysql_metircs(q24)
    results25=mysql_metircs(q25)

    timestamp=datetime.datetime.now()
    
    
    # 获取 Pod 指标并解析
    metrics_output = get_pod_metrics()
    # print(metrics_output)
    pod_metrics = parse_kubectl_top_output(metrics_output)
    # print(pod_metrics)
    
    #处理mysql指标数据
    r1=handle_results(results1)
    # r2=handle_results(results2)
    r3=handle_results(results3)
    r4=handle_results(results4)

    r5=handle_results(results5)
    r6=handle_results(results6)
    r7=handle_results(results7)

    r8=handle_results(results8)
    r9=handle_results(results9)
    r10=handle_results(results10)

    r11=handle_results(results11)
    r12=handle_results(results12)


    r13=handle_results(results13)
    r14=handle_results(results14)
    r15=handle_results(results15)

    r16=handle_results(results16)
    r16['mysql-0'] = '0'

    r17=handle_results(results17)
    r18=handle_results(results18)

    r19=handle_results(results19)
    r20=handle_results(results20)
    r21=handle_results(results21)

    r22=handle_results(results22)
    r23=handle_results(results23)

    r24=handle_results(results24)
    r25=handle_results(results25)

    label=0
    if timestamp.hour in abnormal_hours_1:
        minute=timestamp.minute%5
        if minute in range(0,3):
            label=1
        else:
            label=0
    elif timestamp.hour in abnormal_hours_2:
        minute=timestamp.minute%10
        if minute in range(0,6):
            label=1
        else:
            label=0
    else:
        label=0
    
    print(pod_metrics)

    for pod in pod_metrics:
        pod_name = pod['pod_name']
        print(pod_name)

        try:
            with open("/home/yyy/mysql/data/metrics/"+pod_name+"_metrics.txt",'a') as file1:
                file1.write(f"{timestamp},{pod['cpu']},{pod['memory']},")
                file1.write(f"{r1[pod_name]},{disk_usage},{r3[pod_name]},{r4[pod_name]},{r5[pod_name]},")
                file1.write(f"{r6[pod_name]},{r7[pod_name]},{r8[pod_name]},{r9[pod_name]},{r10[pod_name]},")
                file1.write(f"{r11[pod_name]},{r12[pod_name]},{r13[pod_name]},{r14[pod_name]},{r15[pod_name]},")
                file1.write(f"{r16[pod_name]},{r17[pod_name]},{r18[pod_name]},{r19[pod_name]},{r20[pod_name]},")
                file1.write(f"{r21[pod_name]},{r22[pod_name]},{r23[pod_name]},{r24[pod_name]},{r25[pod_name]},")
                file1.write(f"{label}\n")
        except:
            with open("/home/yyy/mysql/data/metrics/"+pod_name+"_metrics.txt",'a') as file1:
                file1.write(f"{timestamp},pod_unconnect,1\n")



# 创建后台调度器
scheduler = BackgroundScheduler()


def init():
    pkill_commond = "pkill -f kubectl"
    run_command(pkill_commond)

    if not os.path.exists("data/metrics"):
        os.makedirs("data/metrics")
        

    # 删除原来所有数据
    pod_names=["mysql-0","mysql-1","mysql-2","mysql-3","mysql-4","mysql-5","mysql-6"]
    metrics_names="timestamp\t\t\t\t\tcpu,memory,qps,disk_usage,memory_usage,iops,slow_queries,select_full_join,select_scan,threads_created,aborted_connects,aborted_clients,table_locks_waited,innodb_row_lock_waits,innodb_buffer_pool_read_requests,innodb_buffer_pool_reads,innodb_buffer_pool_write_requests,seconds_behind_master,connections,max_used_connections,qcache_hits,qcache_inserts,qcache_lowmem_prunes,created_tmp_tables,created_tmp_disk_tables,binlog_cache_disk_use,binlog_cache_use,label"
    for pod_name in pod_names:
        with open("/home/yyy/mysql/data/metrics/"+pod_name+"_metrics.txt",'w') as file1:
            file1.write(f"{metrics_names}\n")


    # 启动prometheus监听窗口
    prometheus_connect="kubectl port-forward -n monitoring svc/prometheus-service 9091:9091 &"
    run_command(prometheus_connect)



def get_all():
    # 移除之前添加过的所有任务，避免重复添加（如果有需要重新配置任务的情况）
    scheduler.remove_all_jobs()


    # 定时执行一次任务
    scheduler.add_job(job, 'cron', second='*/2')

    # 获取当前时间和结束时间
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(days=7)


    scheduler.start()
    try:
        # 保持主程序运行，让调度器可以在后台持续工作
        while datetime.datetime.now() < end_time:
            time.sleep(1)  # 避免 CPU 占用过高
        print("Reached end time. Shutting down scheduler.")
    except (KeyboardInterrupt, SystemExit):
        # 当接收到中断信号（如Ctrl+C）时，关闭调度器
        print("Received interrupt signal. Shutting down scheduler.")
    finally:
        # 无论是否达到结束时间或接收到中断信号，都关闭调度器
        scheduler.shutdown()
        cursor.close()
        connection.close()
        print("Scheduler and database connection closed.")





if __name__ == '__main__':

    # pkill_commond = "pkill -f kubectl"
    # run_command(pkill_commond)

    # job()


    init()

    get_all()


