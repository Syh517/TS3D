import requests

# Prometheus 的 URL
prometheus_url = "http://localhost:9091/api/v1/query"


# 查询指标数据
# query = 'mysql_global_status_threads_connected'
query = 'mysql_global_status_questions'


response = requests.get(prometheus_url, params={'query': query})

# 检查响应状态码
if response.status_code == 200:
    # 获取指标数据
    metrics = response.json()
    # print(response.text)
                
    
    # 检查查询是否成功
    if metrics['status'] == 'success':
        # 提取数据
        results = metrics['data']['result']
        
        # 打印规整后的指标数据
        for result in results:
            metric_name = result['metric']['__name__']
            instance = result['metric']['instance']
            job = result['metric']['job']
            timestamp = result['value'][0]
            value = result['value'][1]
            
            print(f"Metric: {metric_name}, Instance: {instance}, Job: {job}, Timestamp: {timestamp}, Value: {value}")
    else:
        print(f"Query failed: {metrics['status']}")
    
else:
    print(f"Failed to fetch metrics: {response.status_code}")



