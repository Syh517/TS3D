import subprocess
import time

def run_command_1(command):
    try:
        # 使用 subprocess.run 执行命令，并捕获输出
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("kubectl 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，捕获异常并返回错误信息
        print(f"kubectl 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"
    
def run_command_2(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print("kubectl 命令执行成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"kubectl 命令执行失败: {e}")
        return f"Command failed with error: {e.stderr}"
    


def test():
    # 定义要执行的 kubectl 命令
    kubectl_command_1 = ["kubectl", "get", "pods", "-o", "wide"]
    kubectl_command_2 = "kubectl get pods -o wide"

    # 执行命令并获取输出
    output1 = run_command_1(kubectl_command_1)
    output2 = run_command_2(kubectl_command_2)


    # 打印输出
    print("output1:", output1)
    print("output2:", output2)


def apply_all():
    run_command_2("kubectl apply -f network-delay.yaml")
    run_command_2("kubectl apply -f memory-stress.yaml")
    run_command_2("kubectl apply -f cpu-stress.yaml")
    run_command_2("kubectl apply -f io-stress.yaml")
    run_command_2("kubectl apply -f network-partition.yaml")
    run_command_2("kubectl apply -f pod-failure.yaml")





delete1='kubectl patch networkchaos network-delay -p \'{"metadata":{"finalizers":null}}\' --type=merge'
delete2='kubectl patch stresschaos memory-stress -p \'{"metadata":{"finalizers":null}}\' --type=merge'
delete3='kubectl patch stresschaos cpu-stress -p \'{"metadata":{"finalizers":null}}\' --type=merge'
delete4='kubectl patch iochaos io-stress -p \'{"metadata":{"finalizers":null}}\' --type=merge'
delete5='kubectl patch networkchaos network-partition -p \'{"metadata":{"finalizers":[]}}\' --type=merge'
delete6='kubectl patch podchaos pod-failure -p \'{"metadata":{"finalizers":[]}}\' --type=merge'
def delete_all_1():
    run_command_2(delete1)
    run_command_2(delete2)
    run_command_2(delete3)
    run_command_2(delete4)
    run_command_2(delete5)
    run_command_2(delete6)  

def delete_all_2():
    run_command_2("kubectl delete -f network-delay.yaml")
    run_command_2("kubectl delete -f memory-stress.yaml")
    run_command_2("kubectl delete -f cpu-stress.yaml")
    run_command_2("kubectl delete -f io-stress.yaml")
    run_command_2("kubectl delete -f network-partition.yaml")
    run_command_2("kubectl delete -f pod-failure.yaml") 

  
def c1():
    run_command_2("kubectl apply -f network-delay.yaml")
    run_command_2(delete1)
    run_command_2("kubectl delete -f network-delay.yaml")

def c2():
    run_command_2("kubectl apply -f memory-stress.yaml")
    run_command_2(delete2)
    run_command_2("kubectl delete -f memory-stress.yaml")

def c3():
    run_command_2("kubectl apply -f cpu-stress.yaml")
    run_command_2(delete3)
    run_command_2("kubectl delete -f cpu-stress.yaml")

def c4():
    run_command_2("kubectl apply -f io-stress.yaml")
    run_command_2(delete4)
    run_command_2("kubectl delete -f io-stress.yaml")

def c5():
    run_command_2("kubectl apply -f network-partition.yaml")
    run_command_2(delete5)
    run_command_2("kubectl delete -f network-partition.yaml")

def c6():
    run_command_2("kubectl apply -f pod-failure.yaml")
    run_command_2(delete6)
    run_command_2("kubectl delete -f pod-failure.yaml")    

def show_all():
    print(run_command_2("kubectl get networkchaos"))
    print(run_command_2("kubectl get stresschaos"))
    print(run_command_2("kubectl get iochaos"))
    print(run_command_2("kubectl get podchaos"))    

if __name__ == "__main__":

    # apply_all()

    # delete_all_1()
    # delete_all_2()

    c1()
    c2()
    c3()
    c4()
    c5()
    c6()


    show_all()



    