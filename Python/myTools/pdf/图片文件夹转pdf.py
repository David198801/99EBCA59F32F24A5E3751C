# -*- coding: utf-8 -*-
import sys
import os
from PIL import Image

# --- 配置 ---
# 支持的图片文件扩展名 (可以根据需要添加或删除)
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')

def create_pdf_from_folder(folder_path):
    """
    从指定的文件夹中读取所有图片，按文件名排序后，生成一个PDF文件。
    """
    # 1. 检查输入路径是否为文件夹
    if not os.path.isdir(folder_path):
        print(f"错误: '{folder_path}' 不是一个有效的文件夹。")
        return

    # 2. 获取文件夹中的所有图片文件
    image_files = []
    for filename in os.listdir(folder_path):
        # 检查文件扩展名是否在支持的格式列表中
        if filename.lower().endswith(SUPPORTED_FORMATS):
            image_files.append(os.path.join(folder_path, filename))

    # 3. 如果没有找到图片，则退出
    if not image_files:
        print(f"在文件夹 '{folder_path}' 中没有找到支持的图片文件。")
        print(f"支持的格式为: {SUPPORTED_FORMATS}")
        return

    # 4. 按文件名对图片进行排序
    # image_files.sort() #不排序，按系统默认顺序
    
    # 提示：如果你的文件名是 image1.jpg, image10.jpg, image2.jpg 这种，
    # sort() 会排序成 image1.jpg, image10.jpg, image2.jpg。
    # 如果需要自然排序 (image1, image2, image10)，请取消下面 natsort 相关的注释
    # 并通过 'pip install natsort' 安装 natsort 库。
    # from natsort import natsorted
    # image_files = natsorted(image_files)

    print(f"找到了 {len(image_files)} 张图片，将按以下顺序合并：")
    for i, file in enumerate(image_files):
        print(f"{i+1}: {os.path.basename(file)}")

    # 5. 定义输出PDF的文件名和路径
    # PDF将与输入的文件夹同名，并保存在同一目录下
    # 例如，拖入 D:\MyPics\旅行照片 -> 生成 D:\MyPics\旅行照片.pdf
    pdf_output_path = folder_path + ".pdf"

    # 6. 将图片转换为PDF
    try:
        # 打开第一张图片
        first_image = Image.open(image_files[0])
        # 将第一张图片转换为RGB模式，以避免某些图片格式（如RGBA, P）引发的问题
        first_image_rgb = first_image.convert('RGB')

        # 创建一个空列表来存放剩余的图片对象
        other_images_rgb = []
        for image_path in image_files[1:]:
            img = Image.open(image_path)
            # 同样转换为RGB模式
            other_images_rgb.append(img.convert('RGB'))

        # 保存为PDF
        # 使用 save_all=True 和 append_images 来将多张图片保存到一个PDF文件中
        first_image_rgb.save(
            pdf_output_path, 
            "PDF", 
            resolution=100.0, 
            save_all=True, 
            append_images=other_images_rgb
        )
        print("\n========================================")
        print(f"🎉 成功！PDF已生成：")
        print(f"{pdf_output_path}")
        print("========================================")

    except Exception as e:
        print(f"\n生成PDF时发生错误: {e}")


if __name__ == '__main__':
    # 当文件/文件夹被拖到脚本上时，它的路径会作为命令行参数传递进来
    if len(sys.argv) > 1:
        # 获取拖拽进来的第一个路径
        input_path = sys.argv[1]
        create_pdf_from_folder(input_path)
    else:
        # 如果直接运行脚本，没有拖拽文件，则给出提示
        print("请将一个图片文件夹拖拽到这个脚本文件上以生成PDF。")

    # 在命令行窗口停留30秒，方便用户查看输出信息
    import time
    print("\n此窗口将在30秒后自动关闭...")
    time.sleep(30)

