from kubernetes import client, config

def get_pod_logs(namespace, pod_name, container_name):
    # 加载 Kubernetes 配置
    config.load_kube_config()

    # 创建 CoreV1Api 客户端
    v1 = client.CoreV1Api()

    # 获取 Pod 的日志
    try:
        pod_logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container_name)
        print(pod_logs)
    except client.exceptions.ApiException as e:
        print(f"Exception when calling CoreV1Api->read_namespaced_pod_log: {e}\n")

if __name__ == "__main__":
    namespace = "default"  # 替换为你的命名空间
    pod_name = "mysql-0"    # 替换为你的 Pod 名称
    container_name = "mysql"  # 替换为你的容器名称

    get_pod_logs(namespace, pod_name, container_name)