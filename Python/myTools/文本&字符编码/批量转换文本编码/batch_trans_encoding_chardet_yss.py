import os
import codecs
import chardet


directory_to_convert = r'C:\Users\LiuZhongbin\Desktop\222'
exts = ["txt","sql"]
target_encoding = 'gbk'
yst_bytes = b'\x45\x2D\x53\x61\x66\x65\x4E\x65\x74'

def special(content):
    if content:
        content = content.replace("\xa0"," ").replace("\uf0d8"," ") #处理非ascii空格
        content = content.replace("\u200b","")#处理0宽度字符
        
        #特殊处理一些生僻字，可能本来就有部分编码错误
        content = content.replace("\ue582","")
    return content
    
def special_encoding(encoding):
    if encoding and encoding.lower()=="gb2312":
        encoding = 'gbk'
    return encoding

def convert_file_encoding(file_path):
    
    #识别编码
    result = None
    with open(file_path,"rb") as txt:
        r = txt.read(1024 * 1024)
        if yst_bytes in r:
            print(f"[被加密]: {file_path}")
            return
        result = chardet.detect(r)
        
    if (not result or not result["encoding"] or result["confidence"]<0.99):
        print(f"[识别编码失败]: {file_path}")
        print(result)
        return
        
    encoding = special_encoding(result["encoding"])
    
    if encoding==target_encoding:
        return
    
    # 读取原文件内容
    content = ""
    with codecs.open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
        content = special(content)

    if content:
        # 写入临时文件
        temp_file_path = file_path + '.tmp'
        try:
            # 转换编码
            #converted_content = content.encode('gbk', errors='ignore')
            converted_content = content.encode(target_encoding)
            with codecs.open(temp_file_path, 'wb') as f:
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
            if file.lower().split(".")[-1] in exts:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path)!=0:
                    convert_file_encoding(file_path)

if __name__ == "__main__":
    batch_convert_files(directory_to_convert)
    print("[done]")




