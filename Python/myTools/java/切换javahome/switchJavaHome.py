import winreg
import ctypes
import sys
import os

def run_as_admin():
    # 检查当前进程是否以管理员身份运行
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # 如果不是管理员权限，则使用ShellExecute函数以管理员身份重新运行脚本
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        # 退出当前进程
        sys.exit()

# def set_java_home(java_home_path):
    # try:
        # # 打开Windows注册表中的"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"路径
        # key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS)
        
        # # 设置JAVA_HOME变量为指定的路径
        # winreg.SetValueEx(key, "JAVA_HOME", 0, winreg.REG_SZ, java_home_path)
        
        # # 刷新环境变量
        # winreg.SendMessage(winreg.HWND_BROADCAST, winreg.WM_SETTINGCHANGE, 0, "Environment")
        
        # # 关闭注册表
        # winreg.CloseKey(key)
        
        # print("JAVA_HOME已成功设置为：", java_home_path)
    # except Exception as e:
        # print("设置JAVA_HOME时出现错误：", str(e))

def set_java_home(java_home_path):
    cmd = 'SETX JAVA_HOME "'+java_home_path+'"'
    os.system(cmd)



# 调用函数请求管理员权限
#run_as_admin()

l = []
with open("javahome.txt","r") as txt:
    l = [x.replace('\n','') for x in txt.readlines()]
    for i in range(len(l)):
        print("[" + str(i) + "] " + l[i])
s = input()
jh = l[int(s)]

# 调用函数设置JAVA_HOME路径
set_java_home(jh)
