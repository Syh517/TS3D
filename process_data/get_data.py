from kubernetes import client, config
import schedule
import time
import requests
import os
import subprocess
import json

# 加载 kubeconfig 配置
config.load_kube_config()

# 初始化 API 客户端
core_api = client.CoreV1Api()  # 用于获取日志

# 指定命名空间
namespace = 'default'

# Prometheus 的 URL
prometheus_url = "http://localhost:9091/api/v1/query"

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

    results1=mysql_metircs(q1)
    results2=mysql_metircs(q2)
    results3=mysql_metircs(q3)
    results4=mysql_metircs(q4)

    # print(results1)
    # print(results2)
    # print(results3)
    # print(results4)
    
    
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
    # print(r1)
    # print(r2)
    # print(r3)
    # print(r4)


    for pod in pod_metrics:
        pod_name = pod['pod_name']

        timestamp=int(r1['timestamp'])
        # print('timestamp:',timestamp)
        print(pod_name)
        
        with open("data/metrics/"+pod_name+"_metrics.txt",'w') as file1:
            # 获取并写入pod的指标数据
            # file1.write("指标:\n")
            file1.write(f"timestamp: {timestamp}\t")
            file1.write(f"CPU: {pod['cpu']}\t")
            file1.write(f"memory: {pod['memory']}\t")
            file1.write(f"{r1['metric']}: {r1[pod_name]}\t")
            file1.write(f"{r2['metric']}: {r2[pod_name]}\t")
            file1.write(f"{r3['metric']}: {r3[pod_name]}\t")
            file1.write(f"{r4['metric']}: {r4[pod_name]}\t")
            
            file1.write("\n")
            
        with open("data/logs/"+pod_name+"_logs.txt",'w') as file2:    
            # 获取并写入pod的日志
            # timestamp2=time.time()
            # print('timestamp2:',timestamp2)
            file2.write(f"timestamp: {timestamp}\n")
            log = core_api.read_namespaced_pod_log(name=pod_name, namespace=namespace, container='mysql')
            file2.write("日志:\n")
            file2.write(log + "\n")
            file2.write("\n\n\n")


if __name__ == '__main__':
    directory1 = "data/metrics"
    directory2 = "data/logs"

    if not os.path.exists("data/metrics"):
        os.makedirs("data/metrics")
        
    if not os.path.exists("data/logs"):
        os.makedirs("data/logs")
    
    job()


    # # 每分钟执行一次任务
    # # schedule.every(1).minutes.do(job)
    # schedule.every(1).seconds.do(job)

    # # 持续运行调度器
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

