import os

# ====== 硬编码配置 ======
ROOT_DIR = r"E:\BaiduNetdiskDownload\temp\莫问天机\新建文件夹"   # 改成你的目标路径
FILE_ENCODING = "utf-8"            # 改成你的文件编码，例如 gbk / utf-8
# =======================


def get_all_txt_files(root_dir):
    txt_files = []
    for current_root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".txt"):
                txt_files.append(os.path.join(current_root, file))
    return txt_files


def replace_in_file(file_path, old_text, new_text, encoding):
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()

        if old_text not in content:
            return False

        new_content = content.replace(old_text, new_text)

        with open(file_path, "w", encoding=encoding) as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"处理文件失败: {file_path}, 错误: {e}")
        return False


def batch_replace(root_dir, encoding, old_text, new_text):
    txt_files = get_all_txt_files(root_dir)
    print(f"共找到 {len(txt_files)} 个 txt 文件")

    changed_count = 0
    for file_path in txt_files:
        if replace_in_file(file_path, old_text, new_text, encoding):
            print(f"已修改: {file_path}")
            changed_count += 1

    print(f"替换完成，共修改 {changed_count} 个文件")


def main():
    if not os.path.exists(ROOT_DIR):
        print(f"路径不存在: {ROOT_DIR}")
        return

    print("程序已启动。请输入替换规则，格式为: a,b")
    print("输入 exit 或 quit 退出程序")

    while True:
        user_input = input("请输入: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("程序退出")
            break

        if "," not in user_input:
            print("输入格式错误，请使用: a,b")
            continue

        old_text, new_text = user_input.split(",", 1)

        if old_text == "":
            print("被替换内容不能为空")
            continue

        batch_replace(ROOT_DIR, FILE_ENCODING, old_text, new_text)


if __name__ == "__main__":
    main()