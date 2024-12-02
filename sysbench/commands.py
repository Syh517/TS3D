from kubernetes import client, config
from kubernetes.stream import stream

# 加载Kubernetes配置
config.load_kube_config()

# 创建API实例
api_instance = client.CoreV1Api()

# Pod名称和命名空间
pod_name = "sysbench-pod"
namespace = "default"


def prepare_sysbench(mysql_host, table_size, tables):
    sysbench_cmd = [
        "sysbench",
        "--db-driver=mysql",
        f"--mysql-host={mysql_host}",
        # "--mysql-port=3306",
        "--mysql-user=root",
        "--mysql-password=",
        "--mysql-db=first",
        f"--table-size={table_size}",
        f"--tables={tables}",
        "oltp_common",
        "prepare"
    ]
    resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace, command=sysbench_cmd, stderr=True, stdin=False, stdout=True, tty=False)
    print("准备命令执行成功!")
    return resp

def cleanup_sysbench(mysql_host, table_size, tables):
    sysbench_cmd = [
        "sysbench",
        "--db-driver=mysql",
        f"--mysql-host={mysql_host}",
        # "--mysql-port=3306",
        "--mysql-user=root",
        "--mysql-password=",
        "--mysql-db=first",
        f"--table-size={table_size}",
        f"--tables={tables}",
        "oltp_common",
        "cleanup"
    ]
    resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace, command=sysbench_cmd, stderr=True, stdin=False, stdout=True, tty=False)
    print("清除命令执行成功!")
    return resp

def run_sysbench(mysql_host, table_size, tables, threads, time, events, report_interval, type):
    sysbench_cmd = [
        "sysbench",
        "--db-driver=mysql",
        f"--mysql-host={mysql_host}",
        # "--mysql-port=3306",
        "--mysql-user=root",
        "--mysql-password=",
        "--mysql-db=first",
        f"--table-size={table_size}",
        f"--tables={tables}",
        f"--threads={threads}",
        f"--time={time}",
        f"--events={events}",
        f"--report-interval={report_interval}",
        f"{type}",
        "run"
    ]
    resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace, command=sysbench_cmd, stderr=True, stdin=False, stdout=True, tty=False)
    print(type + "命令执行成功!")
    return resp



if __name__ == "__main__":
    # #插入测试
    # prepare_sysbench('10.244.0.150',100000,10)
    # resp=run_sysbench('10.244.0.150',100000,10,16,60,0,5,'oltp_insert')
    # with open("sysbench_report.txt", "w") as f:
    #     f.write(resp)
    # print("输出已保存到 sysbench_report.txt")
    # cleanup_sysbench('10.244.0.150',100000,10)

    # #读测试
    prepare_sysbench('10.244.0.150',100000,10)
    resp=run_sysbench('10.244.0.152',100000,1,16,60,0,5,'oltp_read_only')
    with open("sysbench_report.txt", "w") as f:
        f.write(resp)
    print("输出已保存到 sysbench_report.txt")
    cleanup_sysbench('10.244.0.150',100000,10)
