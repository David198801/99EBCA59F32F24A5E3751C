import os
import re
import time

import requests

download_path = "E:/bestdori/download"
link_txt_path = "E:/bestdori/download.txt"

proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890',
}


def replace_path_char(s):
    return s.replace("/", "／").replace("\\", "＼").replace("?", "？").replace("*", "＊").replace("|", "｜") \
        .replace(":", "：").replace("<", "＜").replace(">", "＞").replace('''"''', '''＂''')

def replace_non_space_characters(input_string):
    # 使用正则表达式替换所有非空格的非字母数字字符
    result = re.sub(r'\s', ' ', input_string)
    return result

def delete_latest_files(directory):
    if not os.path.exists(directory):
        return

    # 存储最新时间的变量和对应的文件列表
    latest_time = 0
    latest_files = []

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 获取文件的创建时间
            create_time = os.path.getctime(file_path)

            # 如果发现新的最新创建时间，更新列表
            if create_time > latest_time:
                latest_time = create_time
                latest_files = [file_path]
            elif create_time == latest_time:
                # 如果是相同的创建时间，添加到列表中
                latest_files.append(file_path)

    # 删除最新创建的文件
    for file_to_delete in latest_files:
        try:
            os.remove(file_to_delete)
            print(f"删除文件: {file_to_delete}")
        except Exception as e:
            print(f"删除文件 {file_to_delete} 时出错: {e}")


def check_and_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def loop():
    link_info_list = []
    with open(link_txt_path, "r", encoding="utf-8") as txt:
        link_info_list = [x.replace("\n", "") for x in txt.readlines() if x]

    delete_latest_files(download_path)

    all_count = len(link_info_list)
    count = 0
    for info in link_info_list:
        count += 1
        sp = info.split("|")
        link = sp[0]
        name = sp[1]
        sentence = "｜".join(sp[2:])

        dir_path = download_path + "/" + name
        check_and_make_dir(dir_path)

        # 文件名 voiceid_句子
        filename = link.split("/")[-1]
        sp = filename.split(".")
        filename = sp[0] + "_" + sentence + "." + sp[1]
        # 替换特殊字符
        filename = replace_path_char(filename).replace("\x08"," ").replace("\t"," ")

        file_path = dir_path + "/" + filename

        if os.path.exists(file_path):
            print("已存在,跳过 " + link)
            continue

        p = count / all_count * 100

        print(f"正在下载[{p:.3f}% {count}/{all_count}] " + link)
        # 在请求之前创建空文件
        if not os.path.exists(file_path):
            open(file_path, 'wb').close()  # 创建一个空的文件
        # time.sleep(0.5)
        response = None
        if proxies:
            response = requests.get(link, stream=True, proxies=proxies)
        else:
            response = requests.get(link, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)


def count_files_in_directory(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count


if __name__ == '__main__':
    while True:
        try:
            complete_num = count_files_in_directory(download_path)
            loop()
            break
        except Exception as e:  # 捕获所有异常
            print(f"发生错误: {e}")
            print("等待后重试...")
            time.sleep(2)  # 等待 n 秒再重试
