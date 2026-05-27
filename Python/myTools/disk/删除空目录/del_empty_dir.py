import os

def delete_empty_folders(path):
    # 遍历目录树，从底层到顶层
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # 如果文件夹为空，则删除
            if not os.listdir(dir_path):
                print(f"Deleting empty folder: {dir_path}")
                os.rmdir(dir_path)

# 测试
if __name__ == "__main__":
    while True:
        path = input("请输入要清理的目录路径: ").strip()
        delete_empty_folders(path)
        print("空文件夹删除完成。")