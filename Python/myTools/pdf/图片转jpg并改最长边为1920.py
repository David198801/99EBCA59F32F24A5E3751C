# -*- coding: utf-8 -*-

import os
from PIL import Image

# --- 配置参数 ---

# 调整后图像的最长边像素值
MAX_SIZE = 1920

# 输出的 JPG 图像质量 (1-100, 推荐 75-95)
JPEG_QUALITY = 85

# 输出目录的名称
OUTPUT_DIR = "output"

# --- 脚本主逻辑 ---

def process_images():
    """
    主函数，执行所有图像处理任务
    """
    # 1. 获取脚本所在目录
    try:
        # __file__ 在作为脚本运行时是绝对或相对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # 在某些交互式环境(如Jupyter)中 __file__ 未定义，使用当前工作目录
        script_dir = os.getcwd()
        
    print(f"脚本正在以下目录中运行: {script_dir}")

    # 2. 创建输出目录
    output_path = os.path.join(script_dir, OUTPUT_DIR)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"已创建输出目录: {output_path}")

    # 3. 遍历目录中的文件
    processed_count = 0
    for filename in os.listdir(script_dir):
        # 检查是否为 png 文件（不区分大小写）
        if filename.lower().endswith('.png'):
            input_file_path = os.path.join(script_dir, filename)
            
            print(f"正在处理: {filename}...")

            try:
                # 使用 'with' 语句确保文件在处理后被正确关闭
                with Image.open(input_file_path) as img:
                    
                    # 4. 如果图像有透明通道(RGBA)或调色板模式(P)，转换为RGB
                    #    JPG格式不支持透明度
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                        
                    # 5. 保持宽高比，调整尺寸
                    width, height = img.size
                    if width > MAX_SIZE or height > MAX_SIZE:
                        if width > height:
                            # 宽度是长边
                            new_width = MAX_SIZE
                            new_height = int(new_width * height / width)
                        else:
                            # 高度是长边或等长
                            new_height = MAX_SIZE
                            new_width = int(new_height * width / height)
                        
                        # 使用高质量的 LANCZOS 算法进行缩放
                        print(f"    - 调整尺寸从 {width}x{height} 到 {new_width}x{new_height}")
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # 6. 构建输出文件名和路径
                    # 去掉原始后缀名 (.png)
                    base_name = os.path.splitext(filename)[0]
                    output_filename = f"{base_name}.jpg"
                    output_file_path = os.path.join(output_path, output_filename)
                    
                    # 7. 保存为JPG
                    img.save(
                        output_file_path, 
                        'jpeg', 
                        quality=JPEG_QUALITY, 
                        optimize=True, # 尝试进一步优化文件大小
                        progressive=True # 渐进式JPG，改善加载体验
                    )
                    
                    processed_count += 1

            except Exception as e:
                print(f"!!! 处理文件 {filename} 时发生错误: {e}")

    print("\n--- 处理完成 ---")
    if processed_count > 0:
        print(f"总共转换了 {processed_count} 个文件。")
        print(f"结果已保存在 '{OUTPUT_DIR}' 目录中。")
    else:
        print("在当前目录未找到任何 PNG 文件。")


if __name__ == "__main__":
    process_images()
