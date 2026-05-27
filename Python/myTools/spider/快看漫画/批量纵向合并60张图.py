import os
import shutil
from PIL import Image

# ====== 硬编码根目录 ======
ROOT_DIR = r"D:\360极速浏览器下载\temp\1区212 快看漫画版\1区212 快看漫画版未合并原图"


def get_expected_filenames():
    return [f"{i:03d}.jpg" for i in range(1, 61)]


def get_next_merge_filename(chapter_dir):
    """
    返回章节目录下下一个可用的 merge_xxx.png 文件名
    """
    index = 1
    while True:
        filename = f"merge_{index:03d}.png"
        filepath = os.path.join(chapter_dir, filename)
        if not os.path.exists(filepath):
            return filepath
        index += 1


def validate_chapter(chapter_dir):
    """
    校验章节目录：
    1. 必须存在 001.jpg ~ 060.jpg
    2. 每张图片都可以正常打开
    """
    expected_files = get_expected_filenames()
    missing_files = []

    for filename in expected_files:
        path = os.path.join(chapter_dir, filename)
        if not os.path.isfile(path):
            missing_files.append(filename)

    if missing_files:
        print(f"[校验失败] 章节目录缺少图片: {chapter_dir}")
        print("缺少文件:", ", ".join(missing_files))
        return False

    # 校验图片能否正常打开
    for filename in expected_files:
        path = os.path.join(chapter_dir, filename)
        try:
            with Image.open(path) as img:
                img.verify()
        except Exception as e:
            print(f"[校验失败] 图片损坏或无法打开: {path}")
            print(f"原因: {e}")
            return False

    print(f"[校验通过] {chapter_dir}")
    return True


def vertical_merge(image_paths, output_path):
    """
    纵向合并多张图片，宽度取最大值，不足宽度居中贴图
    """
    images = []
    try:
        for path in image_paths:
            img = Image.open(path).convert("RGB")
            images.append(img)

        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)

        merged = Image.new("RGB", (max_width, total_height), (255, 255, 255))

        y = 0
        for img in images:
            x = (max_width - img.width) // 2
            merged.paste(img, (x, y))
            y += img.height

        merged.save(output_path, "PNG")
        print(f"[生成] {output_path}")
        return True

    except Exception as e:
        print(f"[失败] 合并图片失败: {output_path}")
        print(f"原因: {e}")
        return False

    finally:
        for img in images:
            try:
                img.close()
            except:
                pass


def convert_to_png(image_path, output_path):
    """
    单张 jpg 转 png
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img.save(output_path, "PNG")
        print(f"[生成] {output_path}")
        return True
    except Exception as e:
        print(f"[失败] 转换 PNG 失败: {image_path}")
        print(f"原因: {e}")
        return False


def move_originals_to_origin(chapter_dir):
    """
    将 001.jpg ~ 060.jpg 移动到 origin 子目录
    """
    origin_dir = os.path.join(chapter_dir, "origin")
    os.makedirs(origin_dir, exist_ok=True)

    for i in range(1, 61):
        filename = f"{i:03d}.jpg"
        src = os.path.join(chapter_dir, filename)
        dst = os.path.join(origin_dir, filename)
        if os.path.exists(src):
            print(f"[移动] {src} -> {dst}")
            shutil.move(src, dst)


def build_tasks(chapter_dir):
    """
    构建处理任务：
    1. 001 + 002
    2. 003 ~ 058 每4张合并
    3. 059 单独转 png
    4. 060 单独转 png
    """
    merge_tasks = []
    single_tasks = []

    # 001 + 002
    merge_tasks.append([
        os.path.join(chapter_dir, "001.jpg"),
        os.path.join(chapter_dir, "002.jpg")
    ])

    # 003 ~ 058 每4张合并
    # 003-006, 007-010, ..., 055-058
    for start in range(3, 59, 4):
        merge_tasks.append([
            os.path.join(chapter_dir, f"{start:03d}.jpg"),
            os.path.join(chapter_dir, f"{start+1:03d}.jpg"),
            os.path.join(chapter_dir, f"{start+2:03d}.jpg"),
            os.path.join(chapter_dir, f"{start+3:03d}.jpg"),
        ])

    # 059、060 直接转换
    single_tasks.append(os.path.join(chapter_dir, "059.jpg"))
    single_tasks.append(os.path.join(chapter_dir, "060.jpg"))

    return merge_tasks, single_tasks


def process_chapter(chapter_dir):
    print(f"\n=== 处理章节目录: {chapter_dir} ===")

    # 先校验，校验不通过不处理
    if not validate_chapter(chapter_dir):
        print(f"[跳过] {chapter_dir}")
        return

    merge_tasks, single_tasks = build_tasks(chapter_dir)
    generated_files = []

    # 执行合并任务
    for group in merge_tasks:
        output_path = get_next_merge_filename(chapter_dir)
        success = vertical_merge(group, output_path)
        if not success:
            print(f"[终止] 章节处理失败: {chapter_dir}")
            for f in generated_files:
                if os.path.exists(f):
                    os.remove(f)
                    print(f"[回滚删除] {f}")
            return
        generated_files.append(output_path)

    # 执行单张转换任务
    for single_task in single_tasks:
        output_path = get_next_merge_filename(chapter_dir)
        success = convert_to_png(single_task, output_path)
        if not success:
            print(f"[终止] 章节处理失败: {chapter_dir}")
            for f in generated_files:
                if os.path.exists(f):
                    os.remove(f)
                    print(f"[回滚删除] {f}")
            return
        generated_files.append(output_path)

    # 全部成功后再移动原图
    move_originals_to_origin(chapter_dir)
    print(f"[完成] {chapter_dir}")


def main():
    if not os.path.isdir(ROOT_DIR):
        print(f"根目录不存在: {ROOT_DIR}")
        return

    for name in os.listdir(ROOT_DIR):
        chapter_dir = os.path.join(ROOT_DIR, name)
        if os.path.isdir(chapter_dir):
            process_chapter(chapter_dir)


if __name__ == "__main__":
    main()