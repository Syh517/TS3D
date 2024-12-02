import requests

def get_pod_metrics(pod_name, namespace):
    url = f'http://localhost:9091/api/v1/query'
    headers = {'Content-Type': 'application/json'}
    
    # query = f'container_network_receive_bytes_total{{pod="{pod_name}", namespace="{namespace}"}}'
    # response = requests.get(url, headers=headers, params={'query': query})
    # response.raise_for_status()  # 检查 HTTP 错误
    # data = response.json()
    # print(data)

    # if data['status'] == 'success' and data['data']['result']:
    #     return data['data']['result'][0]['value'][1]  # 返回接收的字节数
    # else:
    #     print(f"No data found for pod {pod_name} in namespace {namespace}")
    #     return None

    
    # 定义要查询的指标
    metrics = [
        'mysql_global_status_threads_connected',
        'mysql_global_status_threads_running',
        'mysql_global_status_queries',
        'mysql_global_status_slow_queries',
        'mysql_global_status_buffer_pool_pages_data',
        'mysql_global_status_buffer_pool_pages_free',
        'mysql_global_status_innodb_buffer_pool_pages_total',
        'mysql_global_status_innodb_buffer_pool_pages_free',
        'mysql_slave_status_slave_io_running',
        'mysql_slave_status_slave_sql_running'
    ]
    
    results = {}
    
    for metric in metrics:
        query = f'{metric}{{pod="{pod_name}", namespace="{namespace}"}}'
        try:
            response = requests.get(url, headers=headers, params={'query': query})
            response.raise_for_status()  # 检查 HTTP 错误
            data = response.json()
            print(data)
            
            if data['status'] == 'success' and data['data']['result']:
                print("1")
                results[metric] = data['data']['result'][0]['value'][1]  # 返回指标值
            else:
                results[metric] = None
                print("2")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {metric}: {e}")
            print("3")
            results[metric] = None
    
    return results

# 示例调用
pod_name = 'mysql-0'
namespace = 'default'
metrics = get_pod_metrics(pod_name, namespace)
print(metrics)
for metric, value in metrics.items():
    print(f"{metric}: {value}")