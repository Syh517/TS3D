from kubernetes import client, config
import schedule
import time

# 加载 kubeconfig 配置
config.load_kube_config()

# 初始化 API 客户端
core_api = client.CoreV1Api()  # 用于获取日志
custom_api = client.CustomObjectsApi()  # 用于获取指标

# 指定命名空间
namespace = 'default'

def job():
    # 获取指定命名空间下的 pod 指标数据
    pod_metrics = custom_api.list_namespaced_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        namespace=namespace,
        plural="pods"
    )

    with open("pod_data_and_logs.txt", "a") as file:
        for pod in pod_metrics['items']:
            pod_name = pod['metadata']['name']
            container_name=pod['containers'][0]['name']
            if pod_name=="sysbench-pod":
                continue
            file.write(f"Pod: {pod_name}\n")
            
            # 获取并写入 pod 的指标数据
            file.write("  指标:\n")
            for container in pod['containers']:
                file.write(f"  Container: {container['name']}\n")
                file.write(f"    CPU 使用: {container['usage']['cpu']}\n")
                file.write(f"    内存使用: {container['usage']['memory']}\n")
            
            # 获取并写入 pod 的日志
            try:
                log = core_api.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container_name)
                file.write("  日志:\n")
                file.write(log + "\n")
            except Exception as e:
                file.write("  无法获取日志: " + str(e) + "\n")
            
            file.write("\n")  # 每个 pod 信息之间空一行

job()

# # 每分钟执行一次任务
# schedule.every(1).minutes.do(job)

# # 持续运行调度器
# while True:
#     schedule.run_pending()
#     time.sleep(1)
