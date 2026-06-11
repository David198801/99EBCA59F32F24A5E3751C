import os
from PIL import Image

# ====== 硬编码输入输出目录 ======
INPUT_ROOT = r"D:\code\99EBCA59F32F24A5E3751C\Python\myTools\spider\爱奇艺叭嗒\downloads\嘻哈小天才"
OUTPUT_ROOT = r"D:\code\99EBCA59F32F24A5E3751C\Python\myTools\spider\爱奇艺叭嗒\downloads\嘻哈小天才(爱奇艺叭嗒)"


def merge_vertical(img1_path, img2_path, output_path):
    """将两张图片纵向拼接后保存"""
    img1 = Image.open(img1_path).convert("RGBA")
    img2 = Image.open(img2_path).convert("RGBA")

    width = max(img1.width, img2.width)
    height = img1.height + img2.height

    canvas = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    canvas.paste(img1, (0, 0))
    canvas.paste(img2, (0, img1.height))

    canvas.save(output_path, "WEBP")


def save_single(img_path, output_path):
    """单张图片直接保存"""
    img = Image.open(img_path).convert("RGBA")
    img.save(output_path, "WEBP")


def main():
    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    # 获取输入目录的直接子目录作为标题目录
    title_dirs = [
        d for d in os.listdir(INPUT_ROOT)
        if os.path.isdir(os.path.join(INPUT_ROOT, d))
    ]

    # 按字符串顺序遍历标题目录
    for title in sorted(title_dirs):
        input_title_dir = os.path.join(INPUT_ROOT, title)
        output_title_dir = os.path.join(OUTPUT_ROOT, title)
        os.makedirs(output_title_dir, exist_ok=True)

        # 获取标题目录下的 webp 文件，并按字符串顺序排序
        webp_files = [
            f for f in os.listdir(input_title_dir)
            if os.path.isfile(os.path.join(input_title_dir, f))
            and f.lower().endswith(".webp")
        ]
        webp_files.sort()

        output_index = 1
        i = 0

        while i < len(webp_files):
            output_name = f"{output_index:03d}.webp"
            output_path = os.path.join(output_title_dir, output_name)

            # 每两个文件合并
            if i + 1 < len(webp_files):
                img1_path = os.path.join(input_title_dir, webp_files[i])
                img2_path = os.path.join(input_title_dir, webp_files[i + 1])
                merge_vertical(img1_path, img2_path, output_path)
                print(f"合并: {title} / {webp_files[i]} + {webp_files[i + 1]} -> {output_name}")
                i += 2
            else:
                # 如果最后剩一张，则直接保存
                img_path = os.path.join(input_title_dir, webp_files[i])
                save_single(img_path, output_path)
                print(f"单张: {title} / {webp_files[i]} -> {output_name}")
                i += 1

            output_index += 1

    print("处理完成")


if __name__ == "__main__":
    main()