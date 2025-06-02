import traceback

import requests
import os
import json

proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890',
}

session = requests.Session()

# 设置代理
session.proxies.update(proxies)



def download(url, download_path):
    dir_path = os.path.dirname(download_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    while True:
        try:
            with open(download_path, 'wb') as fb:
                data = session.get(url).content
                fb.write(data)
                fb.close()
            break
        except Exception:
            with open(download_path, 'wb') as f:
                pass  # 不写入任何内容，文件大小为0
            traceback.print_exc()
            print("重试：" + url)
            continue


def store_l2d(out_path,tmp):
    print("正在下载 " + tmp)

    url = f'https://bestdori.com/assets/jp/live2d/chara/{tmp}_rip/buildData.asset'
    buildData = None
    while True:
        try:
            buildData = session.get(url).content
            break
        except Exception:
            traceback.print_exc()
            print("重试：" + url)
            continue

    data = json.loads(buildData)

    model_mark = {
        "version": "Sample 1.0.0",
        "layout": {
            "center_x": 0,
            "center_y": 0,
            "width": 2
        },
        "hit_areas_custom": {
            "head_x": [
                -0.25,
                1
            ],
            "head_y": [
                0.25,
                0.2
            ],
            "body_x": [
                -0.3,
                0.2
            ],
            "body_y": [
                0.3,
                -1.9
            ]
        }
    }

    ## 以下部分为照葫芦画瓢处理成webgal和live2dviewer可读json格式
    Base = data['Base']

    model = Base['model']
    fileName = model['fileName'].replace('.bytes', '')
    bundleName = model['bundleName']
    filePath = f"{bundleName}_rip"

    download_path = f"{out_path}/{tmp}/{filePath}/{fileName}"
    url = f"https://bestdori.com/assets/jp/{bundleName}_rip/{fileName}"
    download(url,download_path)

    model_mark['model'] = f"{filePath}/{fileName}"

    physics = Base['physics']
    fileName = physics['fileName']
    bundleName = physics['bundleName']
    filePath = f"{bundleName}_rip"

    download_path = f"{out_path}/{tmp}/{filePath}/{fileName}"
    url = f"https://bestdori.com/assets/jp/{bundleName}_rip/{fileName}"
    download(url,download_path)

    model_mark['physics'] = f"{filePath}/{fileName}"
    
    textures = Base['textures']
    model_mark['textures'] = []
    for texture in textures:
        fileName = texture['fileName']
        if not fileName.endswith('.png'):
            fileName = fileName + '.png'
        bundleName = texture['bundleName']
        filePath = f"{bundleName}_rip"

        download_path = f"{out_path}/{tmp}/{filePath}/{fileName}"
        url = f"https://bestdori.com/assets/jp/{bundleName}_rip/{fileName}"
        download(url, download_path)
        model_mark['textures'].append(f"{filePath}/{fileName}")

    transition = Base['transition']
    fileName = transition['fileName']
    bundleName = transition['bundleName']
    filePath = f"{bundleName}_rip"

    download_path = f"{out_path}/{tmp}/{filePath}/{fileName}"
    url = f"https://bestdori.com/assets/jp/{bundleName}_rip/{fileName}"
    download(url, download_path)

    motions = Base['motions']
    model_mark['motions'] = {}
    for motion in motions:
        fileName = motion['fileName'].replace('.bytes', '')
        bundleName = motion['bundleName']
        filePath = f"{bundleName}_rip"

        download_path = f"{out_path}/{tmp}/{filePath}/{fileName}"
        url = f"https://bestdori.com/assets/jp/{bundleName}_rip/{fileName}"
        download(url, download_path)

        motion_name = fileName.split('.')[0]
        model_mark['motions'][motion_name] = [{"file": f"{filePath}/{fileName}"}]

    expressions = Base['expressions']
    model_mark['expressions'] = []
    for expression in expressions:
        fileName = expression['fileName']
        bundleName = expression['bundleName']
        filePath = f"{bundleName}_rip"

        download_path = f"{out_path}/{tmp}/{filePath}/{fileName}"
        url = f"https://bestdori.com/assets/jp/{bundleName}_rip/{fileName}"
        download(url, download_path)

        expression_name = fileName.split('.')[0]
        model_mark['expressions'].append({"name": expression_name, "file": f"{filePath}/{fileName}"})

    with open(f'{out_path}/{tmp}/model.json', 'w') as fb:
        fb.write(json.dumps(model_mark))
        fb.close()

    session.close()
    print("处理结束")

