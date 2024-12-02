import requests
from prometheus_client.parser import text_string_to_metric_families

# 替换为 MySQL Exporter 的 URL
mysql_exporter_url = "http://localhost:9104"

def fetch_metrics():
    response = requests.get(mysql_exporter_url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch metrics: {response.status_code}")

def parse_metrics(metrics_text):
    metrics = {}
    for family in text_string_to_metric_families(metrics_text):
        for sample in family.samples:
            metric_name = sample.name
            metric_value = sample.value
            metrics[metric_name] = metric_value
    return metrics

def main():
    metrics_text = fetch_metrics()
    print(metrics_text)
    metrics = parse_metrics(metrics_text)
    
    # 获取特定的指标
    disk_usage = metrics.get("mysql_global_status_innodb_buffer_pool_pages_data")
    memory_usage = metrics.get("mysql_global_status_innodb_buffer_pool_bytes_data")
    iops = metrics.get("mysql_global_status_innodb_data_reads")
    
    print(f"Disk Usage: {disk_usage}")
    print(f"Memory Usage: {memory_usage}")
    print(f"IOPS: {iops}")

if __name__ == "__main__":
    main()