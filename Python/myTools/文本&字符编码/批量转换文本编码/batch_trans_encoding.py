import os
import codecs


def convert_file_encoding(file_path):
    content = ""
    try:
        # 读取原文件内容
        with codecs.open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace("\xa0"," ").replace("\uf0d8"," ") #处理非ascii空格
            content = content.replace("\u200b","")#处理0宽度字符
            content = content.replace("\ue582","")#特殊处理一些生僻字，可能本来就有部分编码错误
    except Exception as e:
        #print(f"skip: {file_path}")
        pass

    if content:
        # 写入临时文件
        temp_file_path = file_path + '.tmp'
        try:
            # 转换编码
            #converted_content = content.encode('gbk', errors='ignore').decode('gbk')
            converted_content = content.encode('gbk').decode('gbk')
            with codecs.open(temp_file_path, 'w', encoding='gbk') as f:
                f.write(converted_content)
            # 删除原文件并重命名临时文件
            os.remove(file_path)
            os.rename(temp_file_path, file_path)
        except Exception as e:
            print(f"[转换失败]: {file_path} - {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

def batch_convert_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.sql'):
                file_path = os.path.join(root, file)
                convert_file_encoding(file_path)

if __name__ == "__main__":
    directory_to_convert = r'C:\Users\LiuZhongbin\Desktop\222'
    batch_convert_files(directory_to_convert)
    print("[done]")




