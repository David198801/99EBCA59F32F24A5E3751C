import os
import shutil
import re
from pypinyin import pinyin, Style

# 定义路径常量
SOURCE_PATH = r"E:\BaiduNetdiskDownload\笔趣阁全站网络小说大合集 31w本[txt](2)\玄幻魔法"  # 请修改为你的源文件夹路径
TARGET_PATH = SOURCE_PATH    # 请修改为你的目标文件夹路径

def get_first_valid_char(filename):
    """
    获取文件名中第一个英文/中文/数字字符
    如果是中文则获取拼音首字母
    """
    # 去掉文件扩展名
    name_without_ext = os.path.splitext(filename)[0]
    
    if not name_without_ext:
        return None
    
    # 使用正则表达式查找第一个字母、数字或中文字符
    match = re.search(r'[a-zA-Z0-9\u4e00-\u9fff]', name_without_ext)
    if not match:
        return None  # 没有找到有效字符
    
    first_valid_char = match.group(0)
    
    # 如果是ASCII字符（包括英文字母和数字）
    if ord(first_valid_char) < 128:
        return first_valid_char.upper()  # 转为大写
    else:
        # 对于中文字符，获取拼音首字母
        py = pinyin(first_valid_char, style=Style.FIRST_LETTER)
        if py and py[0] and py[0][0]:
            return py[0][0].upper()  # 转为大写
        else:
            return None  # 无法转换的情况

def create_category_folders():
    """创建分类文件夹"""
    # 创建数字文件夹 (0-9)
    num_folder = os.path.join(TARGET_PATH, "0-9")
    if not os.path.exists(num_folder):
        os.makedirs(num_folder)
    
    # 创建字母文件夹 (A-Z)
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        letter_folder = os.path.join(TARGET_PATH, letter)
        if not os.path.exists(letter_folder):
            os.makedirs(letter_folder)
    
    

def classify_files():
    """分类文件"""
    # 首先创建分类文件夹
    create_category_folders()
    
    # 统计文件数量
    total_files = 0
    processed_files = 0
    
    # 先统计文件总数
    for _, _, files in os.walk(SOURCE_PATH):
        total_files += len(files)
    
    # 遍历源文件夹中的所有文件
    for root, _, files in os.walk(SOURCE_PATH):
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            
            # 获取第一个有效字符
            first_char = get_first_valid_char(file)
            
            # 确定目标文件夹
            if first_char is None:
                target_folder = os.path.join(TARGET_PATH, "其他")
                # 创建其他字符文件夹
                other_folder = os.path.join(TARGET_PATH, "其他")
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
            elif first_char.isdigit():
                target_folder = os.path.join(TARGET_PATH, "0-9")
            elif 'A' <= first_char <= 'Z':
                target_folder = os.path.join(TARGET_PATH, first_char)
                
            
            # 构建目标文件路径
            target_file_path = os.path.join(target_folder, file)
            
            # 如果目标文件已存在，添加计数后缀
            counter = 1
            while os.path.exists(target_file_path):
                name, ext = os.path.splitext(file)
                target_file_path = os.path.join(target_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            # 移动文件
            try:
                shutil.move(file_path, target_file_path)
                processed_files += 1
                print(f"[{processed_files}/{total_files}] 移动文件 '{file}' 到文件夹 '{os.path.basename(target_folder)}'")
            except Exception as e:
                print(f"移动文件 '{file}' 时出错: {str(e)}")

if __name__ == "__main__":
    print("开始文件分类...")
    
    # 确保目标目录存在
    if not os.path.exists(TARGET_PATH):
        os.makedirs(TARGET_PATH)
        
    classify_files()
    print("文件分类完成！")
