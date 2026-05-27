import os
import json
import re


def get_id_info_dict(data, voiceid_info_dict, current_data):
    if current_data is None:
        current_data = {}

    if isinstance(data, dict):
        if 'windowDisplayName' in data:
            current_data['windowDisplayName'] = data['windowDisplayName']
        if 'body' in data:
            # 移除body中的换行符#和|
            current_data['body'] = data['body'].replace('\n', '')#.replace("|", '')
        if 'voiceId' in data:
            current_data['voiceId'] = data['voiceId']

            # 检查所有字段是否非空
            valid_data = all(current_data.get(k) for k in ['windowDisplayName', 'body', 'voiceId'])
            # 检查 windowDisplayName 是否包含 "・"
            valid_displayname = "・" not in current_data.get('windowDisplayName', "")
            # 检查 body 是否只包含标点符号
            valid_body = bool(re.sub(r'[^\w]', '', current_data.get('body', "")))

            # 如果满足所有条件，输出结果到文件
            if valid_data and valid_displayname and valid_body:
                voiceid_info_dict[current_data[
                    'voiceId']] = f"{current_data['windowDisplayName']}|{current_data['body']}\n"
                current_data.clear()  # 清空当前数据以供下次使用

        for key in data:
            get_id_info_dict(data[key], voiceid_info_dict, current_data)
    elif isinstance(data, list):
        for item in data:
            get_id_info_dict(item, voiceid_info_dict, current_data)


# 文件输出路径
download_txt_path = "E:/bestdori/download.txt"

assets_out_path = r"E:/bestdori/asset"
mp3_out_path = r"E:/bestdori/mp3"
mp3_txt_path = mp3_out_path + "/mp3links.txt"

if __name__ == '__main__':

    voiceid_info_dict = {}
    # 遍历所有文件
    for root, dirs, files in os.walk(assets_out_path):
        for f in files:
            if f.endswith(".asset"):
                asset_file_path = os.path.join(root, f)
                content = None
                with open(asset_file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                get_id_info_dict(content, voiceid_info_dict, None)

    filename_link_dict = {}
    # 遍历所有文件
    with open(mp3_txt_path, 'r', encoding='utf-8') as txt:
        l = [x.replace("\n","") for x in txt.readlines()]
        for link in l:
            if link and "/" in link:
                filename = link.split("/")[-1]
                filename_link_dict[filename] = link

    with open(download_txt_path, 'w', encoding='utf-8') as txt:
        for filename in filename_link_dict:
            if "." in filename:
                link = filename_link_dict[filename]
                voiceid = filename.split(".")[0]
                info = voiceid_info_dict.get(voiceid)
                if info:
                    txt.write(f"{link}|{info}")
