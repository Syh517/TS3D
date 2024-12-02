from kubernetes import client, config
from kubernetes.stream import stream

# 加载Kubernetes配置
config.load_kube_config()

# 创建API实例
api_instance = client.CoreV1Api()

# Pod名称和命名空间
pod_name = "sysbench-pod"
namespace = "default"

# SysBench命令
command1 = ["sysbench",
            "--db-driver=mysql",
            "--mysql-host=10.244.0.129",
            "--mysql-port=3306",
            "--mysql-user=root",
            "--mysql-password=",
            "--mysql-db=first",
            "--tables=10",
            "--table-size=100000",
            "oltp_common",
            "prepare"]

command2 = ["sysbench",
            "--db-driver=mysql",
            "--mysql-host=10.244.0.129",
            "--mysql-port=3306",
            "--mysql-user=root",
            "--mysql-password=",
            "--mysql-db=first",
            "--tables=10",
            "--table-size=100000",
            "--threads=16",
            "--time=60",
            "--report-interval=5",
            "oltp_insert",
            "run"]


command3 = ["sysbench",
            "--db-driver=mysql",
            "--mysql-host=10.244.0.129",
            "--mysql-port=3306",
            "--mysql-user=root",
            "--mysql-password=",
            "--mysql-db=first",
            "--tables=10",
            "--table-size=100000",
            "oltp_common",
            "cleanup"]

command4 = ["sysbench",
            "--db-driver=mysql",
            "--mysql-host=10.244.0.131",
            "--mysql-user=root",
            "--mysql-password=",
            "--mysql-db=first",
            "--table-size=1000000",
            "--threads=16",
            "--time=60",
            "--report-interval=10",
            "oltp_read_only",
            "run"]

# 执行命令
try:
    # 使用stream方法执行命令
    resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace, command=command1, stderr=True, stdin=False, stdout=True, tty=False)
    print("命令1执行成功!")
    resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace, command=command2, stderr=True, stdin=False, stdout=True, tty=False)
    print("命令2执行成功!")
     # 将输出保存到文件
    with open("sysbench_report.txt", "w") as f:
        f.write(resp)
    print("输出已保存到 sysbench_report.txt")
    resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace, command=command3, stderr=True, stdin=False, stdout=True, tty=False)
    print("命令3执行成功!")
    
except Exception as e:
    print("命令执行失败：", str(e))