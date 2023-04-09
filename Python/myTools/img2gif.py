import imageio
import glob
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def read_images(image_name_list):
    image_list = []
    size = Image.open(image_name_list[0]).size
    for image_name in image_name_list:
        image = Image.open(image_name).resize(size, Image.ANTIALIAS)

        # 转为UMat，以使用addWeighted方法
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        image_list.append(image)
    # print("图片读取完成")
    return image_list


def create_gif(image_list, gif_name, duration=2, k=9):
    """生成gif动图,
    image_list:图片矩阵列表；
    git_name：生成的gif；
    duration：两张影像之间的间隔时间，单位秒。
    """
    frames = []
    
    for index in range(len(image_list)-1):
        buff = gif_gradually(image_list[index], image_list[index+1], k)
        frames.extend(buff)
        
    # 生成gif,frames是图片列表，duration是间隔时间
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration/k)
    print("gif图制作完成")


def gif_gradually(img1, img2, k=10):
    """生成两张影像之间的过度影像，渐变"""
    buff = []
    for i in range(k):
        alpha = i*1/k
        # 增加权重，显示两张图片之间的过渡图片
        img = cv2.addWeighted(img1, alpha, img2, (1-alpha), gamma=0)

        # 转为PIL
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2RGB)
        buff.append(img)

    return buff

# gif生成
filename_list = glob.glob(r'*.bmp')
image_list = read_images(filename_list)

create_gif(image_list, "test.gif", duration=4, k=36)

