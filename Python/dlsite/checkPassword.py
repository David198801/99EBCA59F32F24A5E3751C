#coding:utf-8
import os
import win_subprocess
import subprocess

name = u"藤堂れんげ"
path = u"G:/音声/" + name + u"/"

def getE(path):
  return os.path.splitext(path)[-1]

for root,dirs,files in os.walk(path):
    for f in files:
        if (getE(f).lower() in [".zip",".rar",".7z"]):
            filePath = os.path.join(root, f)
            cmd = u'''7z l "''' + filePath + u'''"'''
            # cmd = '''"''' + filePath + '''"'''
            # cmd = cmd.encode("utf-8")
            # print cmd
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            # stdout = p.communicate()
            # p.stdin.write("\n")

            # for i in stdout:
            #     if i:
            #         if "Enter password" in i:
            #             print f




# filePath = ur"G:\音声\秋野かえで\RJ248933 被虐願望ネクラJKとらぶらぶド変態えっち…♪\RJ248933.zip"
# filePath = ur"G:\音声\test\新建 Microsoft Word 文档.zip"
# cmd = '''"''' + filePath + '''"'''
# cmd = cmd.encode("utf-8")
# # cmd = '"G:\\\xe9\x9f\xb3\xe5\xa3\xb0\\test\\\xe6\x96\xb0\xe5\xbb\xba Microsoft Word \xe6\x96\x87\xe6\xa1\xa3.zip"'
#
# # p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
# print cmd
# # win_subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
# os.system(cmd)


# else:
            #     try:
            #         p = subprocess.run(cmdt, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            #                            stdin=subprocess.PIPE, timeout=0.5)
            #         if "Enter password" in p.stdout.decode("gbk"):
            #             print(f,"pw")
            #         else:
            #             print(f)
            #     except subprocess.TimeoutExpired:
            #         print(f,"timeout")








            # try:
            #      subprocess.run(cmd,shell=True, stdout=subprocess.STDOUT, timeout=1)
            # except subprocess.TimeoutExpired:
            #     pass

            # p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
            # stdout = p.communicate(timeout=1)
            # for i in stdout:
            #     if i:
            #         print(i)
                    # if b"Enter password" in i:
                    #     print(f)

            # try:
            #     s = p.communicate(timeout=1)
            # except :
            #     p.stdin.write(b"\n")








            # returncode = p.poll()
            #
            # while returncode is None:
            #     print("a")
            #     line = p.stdout.readline()
            #     returncode = p.poll()
            #     line = line.strip()
            #     print(line.decode("gbk"))






