from kubernetes import client, config
import schedule
import time
import requests
import os


# 加载 kubeconfig 配置
config.load_kube_config()

# 初始化 API 客户端
core_api = client.CoreV1Api()  # 用于获取日志
custom_api = client.CustomObjectsApi()  # 用于获取指标

# 指定命名空间
namespace = 'default'

# Prometheus 的 URL
prometheus_url = "http://localhost:9091/api/v1/query"

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
    dict['metric']=results[0]['metric']['__name__']
    dict['timestamp']=results[0]['value'][0]
    for result in results:
        instance = result['metric']['instance']
        dict[instance]=result['value'][1]
    
    return dict
        




def job():
    print("Collecting...")
    #获取mysql指标数据
    q1 = 'mysql_global_status_threads_connected'
    q2 = 'mysql_global_status_questions'
    q3='mysql_global_status_key_read_requests'
    q4='mysql_global_status_key_reads'

    results1=mysql_metircs(q1)
    results2=mysql_metircs(q2)
    results3=mysql_metircs(q3)
    results4=mysql_metircs(q4)
    
    
    # 获取pod系统指标数据
    pod_metrics = custom_api.list_namespaced_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        namespace=namespace,
        plural="pods"
    )
    
    #处理mysql指标数据
    r1=handle_results(results1)
    r2=handle_results(results2)
    r3=handle_results(results3)
    r4=handle_results(results4)


    for pod in pod_metrics['items']:
        pod_name = pod['metadata']['name']
        container_name=pod['containers'][0]['name']
        if pod_name=="sysbench-pod":
            continue

        timestamp=r1['timestamp']
        print(pod_name)
        
        with open("data/metrics/"+pod_name+"_metrics.txt",'a') as file1:
            # 获取并写入pod的指标数据
            # file1.write("指标:\n")
            container=pod['containers'][0]
            print('container:',container)
            file1.write(f"timestamp: {timestamp}\t")
            file1.write(f"CPU: {container['usage']['cpu']}\t")
            file1.write(f"memory: {container['usage']['memory']}\t")
            file1.write(f"{r1['metric']}: {r1[pod_name]}\t")
            file1.write(f"{r2['metric']}: {r2[pod_name]}\t")
            file1.write(f"{r3['metric']}: {r3[pod_name]}\t")
            file1.write(f"{r4['metric']}: {r4[pod_name]}\t")
            
            file1.write("\n")
            
        with open("data/logs/"+pod_name+"_logs.txt",'a') as file2:    
            # 获取并写入pod的日志
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
    # schedule.every(10).seconds.do(job)

    # # 持续运行调度器
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
