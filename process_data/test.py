from kubernetes import client, config
import time
import requests
import os
import subprocess
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# 加载 kubeconfig 配置
config.load_kube_config()

# 初始化 API 客户端
core_api = client.CoreV1Api()  # 用于获取日志

# 指定命名空间
namespace = 'default'

# Prometheus 的 URL
prometheus_url = "http://localhost:9091/api/v1/query"






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
            # if pod_name.startswith("sysbench-pod"):
            #     continue
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

def handle_results(results,metric_name=None):
    dict={}
    if metric_name:
        dict['metric']=metric_name
    else:
        dict['metric']=results[0]['metric']['__name__']
    
    # dict['metric']=results[0]['metric']['__name__']
    dict['timestamp']=results[0]['value'][0]
    for result in results:
        instance = result['metric']['instance']
        dict[instance]=result['value'][1]
    
    return dict
        




def job():
    print("Collecting...")
    #获取mysql指标数据
    q1 = 'rate(mysql_global_status_questions[1m])'
    q2 = 'mysql_global_status_innodb_data_written - mysql_global_status_innodb_data_read + mysql_global_status_innodb_os_log_written' 
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
    results2=mysql_metircs(q2)
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

    # print(results1)
    # print(results2)
    # print(results3)
    # print(results4)
    # print(results5)
    # print(results6)
    # print(results7)
    # print(results8)
    # print(results9)
    # print(results10)


    timestamp=datetime.datetime.now()
    
    
    # 获取 Pod 指标并解析
    metrics_output = get_pod_metrics()
    # print(metrics_output)
    pod_metrics = parse_kubectl_top_output(metrics_output)
    print(pod_metrics)
    
    #处理mysql指标数据
    r1=handle_results(results1, 'qps')
    r2=handle_results(results2, 'disk_usage')
    r3=handle_results(results3, 'memory_usage')
    r4=handle_results(results4, 'iops')

    r5=handle_results(results5, 'slow_queries')
    r6=handle_results(results6, 'select_full_join')
    r7=handle_results(results7, 'select_scan')

    r8=handle_results(results8, 'threads_created')
    r9=handle_results(results9, 'aborted_connects')
    r10=handle_results(results10, 'aborted_clients')

    r11=handle_results(results11, 'table_locks_waited')
    r12=handle_results(results12, 'innodb_row_lock_waits')


    r13=handle_results(results13, 'innodb_buffer_pool_read_requests')
    r14=handle_results(results14, 'innodb_buffer_pool_reads')
    r15=handle_results(results15, 'innodb_buffer_pool_write_requests')

    r16=handle_results(results16, 'seconds_behind_master')
    r16['mysql-0'] = '0'

    r17=handle_results(results17, 'connections')
    r18=handle_results(results18, 'max_used_connections')

    r19=handle_results(results19, 'qcache_hits')
    r20=handle_results(results20, 'qcache_inserts')
    r21=handle_results(results21, 'qcache_lowmem_prunes')

    r22=handle_results(results22, 'created_tmp_tables')
    r23=handle_results(results23, 'created_tmp_disk_tables')

    r24=handle_results(results24, 'binlog_cache_disk_use')
    r25=handle_results(results25, 'binlog_cache_use')


    # print(r1)
    # print(r2)
    # print(r3)
    # print(r4)

    # print(r5)
    # print(r6)
    # print(r7)

    # print(r8)
    # print(r9)
    # print(r10)

    # print(r16)

    


    for pod in pod_metrics:
        pod_name = pod['pod_name']

        # timestamp=int(r1['timestamp'])
        # print('timestamp:',timestamp)
        print(pod_name)
        
        with open("/home/yyy/mysql/data/metrics/"+pod_name+"_metrics.txt",'a') as file1:
            # 获取并写入pod的指标数据
            # file1.write("指标:\n")
            file1.write(f"timestamp: {timestamp}\t")
            file1.write(f"CPU: {pod['cpu']}\t")
            file1.write(f"memory: {pod['memory']}\t")
            file1.write(f"{r1['metric']}: {r1[pod_name]}\t")
            file1.write(f"{r2['metric']}: {r2[pod_name]}\t")
            file1.write(f"{r3['metric']}: {r3[pod_name]}\t")
            file1.write(f"{r4['metric']}: {r4[pod_name]}\t")
            file1.write(f"{r5['metric']}: {r5[pod_name]}\t")
            file1.write(f"{r6['metric']}: {r6[pod_name]}\t")
            file1.write(f"{r7['metric']}: {r7[pod_name]}\t")
            file1.write(f"{r8['metric']}: {r8[pod_name]}\t")
            file1.write(f"{r9['metric']}: {r9[pod_name]}\t")
            file1.write(f"{r10['metric']}: {r10[pod_name]}\t")
            file1.write(f"{r11['metric']}: {r11[pod_name]}\t")
            file1.write(f"{r12['metric']}: {r12[pod_name]}\t")
            file1.write(f"{r13['metric']}: {r13[pod_name]}\t")
            file1.write(f"{r14['metric']}: {r14[pod_name]}\t")
            file1.write(f"{r15['metric']}: {r15[pod_name]}\t")
            file1.write(f"{r16['metric']}: {r16[pod_name]}\t")
            file1.write(f"{r17['metric']}: {r17[pod_name]}\t")
            file1.write(f"{r18['metric']}: {r18[pod_name]}\t")
            file1.write(f"{r19['metric']}: {r19[pod_name]}\t")
            file1.write(f"{r20['metric']}: {r20[pod_name]}\t")
            file1.write(f"{r21['metric']}: {r21[pod_name]}\t")
            file1.write(f"{r22['metric']}: {r22[pod_name]}\t")
            file1.write(f"{r23['metric']}: {r23[pod_name]}\t")
            file1.write(f"{r24['metric']}: {r24[pod_name]}\t")
            file1.write(f"{r25['metric']}: {r25[pod_name]}\t")
            
            file1.write("\n")
            
        # with open("/home/yyy/mysql/data/logs/"+pod_name+"_logs.txt",'a') as file2:    
        #     # 获取并写入pod的日志
        #     # timestamp2=time.time()
        #     # print('timestamp2:',timestamp2)
        #     file2.write(f"timestamp: {timestamp}\n")
        #     log = core_api.read_namespaced_pod_log(name=pod_name, namespace=namespace, container='mysql')
        #     file2.write("日志:\n")
        #     file2.write(log + "\n")
        #     file2.write("\n\n\n")



# 创建后台调度器
scheduler = BackgroundScheduler()


def init():
    if not os.path.exists("data/metrics"):
        os.makedirs("data/metrics")
        
    # if not os.path.exists("data/logs"):
    #     os.makedirs("data/logs")


    # 删除原来所有数据
    pod_names=["mysql-0","mysql-1","mysql-2","mysql-3","mysql-4","mysql-5","mysql-6"]
    for pod_name in pod_names:
        with open("/home/yyy/mysql/data/metrics/"+pod_name+"_metrics.txt",'w') as file1:
            pass

        # with open("/home/yyy/mysql/data/logs/logs.txt",'w') as file2:
        #     pass

    # 启动prometheus监听窗口
    prometheus_connect="kubectl port-forward -n monitoring svc/prometheus-service 9091:9091 &"
    run_command(prometheus_connect)



def get_all():
    # 移除之前添加过的所有任务，避免重复添加（如果有需要重新配置任务的情况）
    scheduler.remove_all_jobs()


    # 定时执行一次任务
    scheduler.add_job(job, 'cron', second='*')

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





if __name__ == '__main__':

    # pkill_commond = "pkill -f kubectl"
    # run_command(pkill_commond)

    init()

    # job()

    get_all()


