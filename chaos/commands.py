import subprocess

def run_kubectl_command_1(command):
    try:
        # 使用 subprocess.run 执行命令，并捕获输出
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("kubectl 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，捕获异常并返回错误信息
        print(f"kubectl 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"
    
def run_kubectl_command_2(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print("kubectl 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"kubectl 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"
    
    
# 定义要执行的 kubectl 命令
kubectl_command_1 = ["kubectl", "get", "pods", "-o", "wide"]
kubectl_command_2 = "kubectl get pods -o wide"

# 执行命令并获取输出
output1 = run_kubectl_command_1(kubectl_command_1)
output2 = run_kubectl_command_2(kubectl_command_2)


# 打印输出
print("output1:", output1)
print("output2:", output2)