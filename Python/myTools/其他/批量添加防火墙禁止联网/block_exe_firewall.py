import os
import subprocess
import sys
import ctypes

def is_admin():
    """检查当前用户是否拥有管理员权限。"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员身份重新运行脚本。"""
    if not is_admin():
        print("正在以管理员权限重新启动...")
        # 以管理员权限重新启动当前脚本
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def add_to_firewall(exe_path):
    try:
        # 添加到防火墙的命令
        command_inbound = f'netsh advfirewall firewall add rule name="{os.path.basename(exe_path)}_inbound" dir=in action=block program="{exe_path}" enable=yes'
        command_outbound = f'netsh advfirewall firewall add rule name="{os.path.basename(exe_path)}_outbound" dir=out action=block program="{exe_path}" enable=yes'
        
        # 执行命令
        subprocess.run(command_inbound, shell=True, check=True)
        subprocess.run(command_outbound, shell=True, check=True)

        print(f'Successfully added {exe_path} to Windows Firewall.')
    except subprocess.CalledProcessError as e:
        print(f'Failed to add {exe_path} to Windows Firewall: {e}')

def search_executables_and_block_firewall(start_path):
    # 递归搜索所有exe文件
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.exe'):
                exe_path = os.path.join(root, file)
                add_to_firewall(exe_path)

if __name__ == "__main__":
    run_as_admin()  # 请求管理员权限
    
    # 获取脚本所在路径
    #path = os.path.dirname(os.path.abspath(__file__))
    path=""
    while True:
        path = input("enter path:")
        if os.path.exists(path):
            search_executables_and_block_firewall(path)
        else:
            print(path + "\n is not exists")