import requests

# def get_pod_metrics(pod_name, namespace):
#     url = f'http://localhost:9091/api/v1/query'
#     headers = {'Content-Type': 'application/json'}
    
#     query = f'container_network_receive_bytes_total{{pod="{pod_name}", namespace="{namespace}"}}'
#     response = requests.get(url, headers=headers, params={'query': query})
#     response.raise_for_status()  # 检查 HTTP 错误
#     data = response.json()
#     print(data)

#     if data['status'] == 'success' and data['data']['result']:
#         return data['data']['result'][0]['value'][1]  # 返回接收的字节数
#     else:
#         print(f"No data found for pod {pod_name} in namespace {namespace}")
#         return None
    


# # 示例调用
# pod_name = 'mysql-0'
# namespace = 'default'
# metrics = get_pod_metrics(pod_name, namespace)
# print(metrics)

# Prometheus 服务器的地址
PROMETHEUS_URL = "http://localhost:9091"

def query_prometheus(query):
    """
    查询 Prometheus 并返回结果
    """
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {
        "query": query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        return response.json()['data']['result']
    else:
        raise Exception(f"Query failed: {response.status_code} - {response.text}")

def get_mysql_metrics():
    """
    获取 MySQL 指标
    """
    # 查询 MySQL 的 up 指标
    up_query = 'mysql_up'
    up_result = query_prometheus(up_query)
    print("MySQL Up Status:")
    for result in up_result:
        print(f"Instance: {result['metric']['instance']}, Value: {result['value'][1]}")

    # 查询 MySQL 的连接数指标
    connections_query = 'mysql_global_status_threads_connected'
    connections_result = query_prometheus(connections_query)
    print("\nMySQL Connections:")
    for result in connections_result:
        print(f"Instance: {result['metric']['instance']}, Value: {result['value'][1]}")

    # 查询 MySQL 的查询数指标
    queries_query = 'mysql_global_status_queries'
    queries_result = query_prometheus(queries_query)
    print("\nMySQL Queries:")
    for result in queries_result:
        print(f"Instance: {result['metric']['instance']}, Value: {result['value'][1]}")

if __name__ == "__main__":
    get_mysql_metrics()