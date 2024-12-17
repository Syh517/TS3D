import multiprocessing
import subprocess

def run_script(script_name):
    # 这个函数将运行一个Python脚本
    subprocess.run(['python3', script_name])

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.stderr}"

if __name__ == '__main__':

    # 创建两个进程
    p1 = multiprocessing.Process(target=run_script, args=('execute.py',))
    p2 = multiprocessing.Process(target=run_script, args=('process_data/get_data.py',))

    # 启动进程
    p1.start()
    p2.start()


    p1.join()
    p2.join()