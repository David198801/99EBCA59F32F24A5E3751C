import os
import threading
import time
import chardet
import codecs
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from tqdm import tqdm  # 使用tqdm显示进度条

directory_to_convert = r'E:\BaiduNetdiskDownload\知轩藏书备份站'

# 需要转换的后缀名
exts = ["txt", "sql"]

# 目标编码
target_encoding = 'gbk'

# 预测编码用的字节数
CHARDET_LEN = 512 * 1024

# 线程数
THREAD_NUM = 16

def special(content):
    if content:
        content = content.replace("\xa0", " ").replace("\uf0d8", " ")  # 处理非ascii空格
        content = content.replace("\u200b", "")  # 处理0宽度字符
        
        # 特殊处理一些生僻字，可能本来就有部分编码错误
        content = content.replace("\ue582", "")
    return content
    
def special_encoding(encoding):
    if encoding and encoding.lower() == "gb2312":
        encoding = 'gbk'
    return encoding

def convert_file_encoding(file_path):
    try:
        # 识别编码
        result = None
        with open(file_path, "rb") as txt:
            r = txt.read(CHARDET_LEN)
            result = chardet.detect(r)
            
        if (not result or not result["encoding"] or result["confidence"] < 0.99):
            print(f"[识别编码失败]: {file_path}")
            print(result)
            return
            
        encoding = special_encoding(result["encoding"])
        
        if encoding == target_encoding:
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
                converted_content = content.encode(target_encoding, errors='ignore')
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
    except Exception as e:
        print(f"[处理文件异常]: {file_path} - {e}")

def batch_convert_files(directory, max_workers):
    """
    使用多线程批量转换文件编码，并显示进度
    
    Args:
        directory: 要处理的目录路径
        max_workers: 最大线程数
    """
    files_to_convert = []
    
    print("扫描文件中...")
    # 首先收集所有需要转换的文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().split(".")[-1] in exts:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) != 0:
                    files_to_convert.append(file_path)
    
    total_files = len(files_to_convert)
    print(f"找到 {total_files} 个文件需要处理")
    
    # 创建一个线程安全的计数器和锁
    counter = {"processed": 0}
    lock = threading.Lock()
    
    def convert_and_update(file_path):
        # 处理文件
        convert_file_encoding(file_path)
        # 更新计数器
        with lock:
            counter["processed"] += 1
    
    # 创建进度条
    pbar = tqdm(total=total_files, desc="处理进度")
    
    # 启动进度更新线程
    stop_flag = threading.Event()
    
    def update_progress():
        last_count = 0
        while not stop_flag.is_set():
            current = counter["processed"]
            if current > last_count:
                pbar.update(current - last_count)
                last_count = current
            time.sleep(0.1)  # 短暂休眠，减少CPU占用
    
    progress_thread = threading.Thread(target=update_progress)
    progress_thread.daemon = True
    progress_thread.start()
    
    try:
        # 使用线程池并行处理文件
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务到线程池
            futures = [executor.submit(convert_and_update, file_path) 
                      for file_path in files_to_convert]
            
            # 等待所有任务完成
            for future in futures:
                future.result()  # 这会抛出任何在线程中发生的异常
    finally:
        # 确保进度条更新线程停止
        stop_flag.set()
        progress_thread.join(timeout=1.0)
        pbar.close()
            
    print(f"成功处理 {counter['processed']} 个文件")
    

if __name__ == "__main__":
    batch_convert_files(directory_to_convert, THREAD_NUM)
    input("[done]")
