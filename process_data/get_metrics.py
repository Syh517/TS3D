from kubernetes import client, config
from kubernetes.client import ApiClient
from kubernetes.client.rest import RESTResponse
import json

# 加载kubeconfig配置
config.load_kube_config()

# 创建CoreV1Api对象
v1 = client.CoreV1Api()
api_client = ApiClient()
print(api_client.configuration.host)                             

# 定义命名空间和Pod名称
namespace_name = 'default'
pod_name = 'mysql-0'

# 获取Pod的指标数据
rest_response: RESTResponse = api_client.request(
    url=api_client.configuration.host +
    f'/apis/metrics.k8s.io/v1beta1/namespaces/{namespace_name}/pods/{pod_name}',
    method='GET'
)
data = rest_response.data
data=json.loads(data)
print(data)

cpu_usage = data['containers'][0]['usage']['cpu']
memory_usage = data['containers'][0]['usage']['memory']

print(f"CPU Usage: {cpu_usage}, Memory Usage: {memory_usage}")