#检查亿赛通加密的文件

import os


# 指定目录路径
directory = r'E:\99EBCA59F32F24A5E3751C'
# 目标字节序列45 2D 53 61 66 65 4E 65 74即E-SafeNet
target_bytes = b'\x45\x2D\x53\x61\x66\x65\x4E\x65\x74'




def search_files(directory, target_bytes,txt):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    if target_bytes in content:
                        txt.write(f"File '{file_path}' contains the target bytes.")
                        txt.write("\n")
            except:
                txt.write("ERR:"+file_path)
                txt.write("\n")


with open("out.txt","a+",encoding='utf-8') as txt:
    search_files(directory, target_bytes,txt)

    
