from kubernetes import client, config
import schedule
import time

# 加载Kubernetes配置
config.load_kube_config()

# 初始化 CustomObjects API
custom_api = client.CustomObjectsApi()

# 指定命名空间
namespace = 'default'

# 定义获取指标数据的函数
def get_metrics_data(namespace):
    # 获取命名空间下的 pod 资源使用情况
    pod_metrics = custom_api.list_namespaced_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        namespace=namespace,
        plural="pods"
    )
    # 打开文件，使用 "a" 模式以追加方式写入
    with open("pod_metrics.txt", "a") as file:
        for pod in pod_metrics['items']:
            pod_name=pod['metadata']['name']
            if pod_name=="sysbench-pod":
                continue
            file.write(f"Pod: {pod['metadata']['name']}\n")
            for container in pod['containers']:
                file.write(f"  Container: {container['name']}\n")
                file.write(f"    CPU 使用: {container['usage']['cpu']}\n")
                file.write(f"    内存使用: {container['usage']['memory']}\n")
            file.write("\n")  # 每个 pod 信息之间空一行
    
    # for pod in pod_metrics['items']:
    #     pod_name=pod['metadata']['name']
    #     if pod_name=="sysbench-pod":
    #         continue
    #     print(f"Pod: {pod['metadata']['name']}")
    #     for container in pod['containers']:
    #         print(f"  Container: {container['name']}")
    #         print(f"    CPU 使用: {container['usage']['cpu']}")
    #         print(f"    内存使用: {container['usage']['memory']}")


get_metrics_data(namespace)
# # 定义要执行的任务
# def job():
#     get_metrics_data(namespace)

# # 设置定时任务，例如每分钟执行一次
# schedule.every(1).minutes.do(job)

# # 无限循环，按计划执行任务
# while True:
#     schedule.run_pending()
#     time.sleep(1)