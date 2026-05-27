import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinterdnd2 import DND_FILES, TkinterDnD


class CommandDropGroup:
    def __init__(self, parent, title, default_cmd, log_func, root):
        self.log = log_func
        self.root = root
        self.frame = tk.LabelFrame(parent, text=title, padx=10, pady=10)

        tk.Label(self.frame, text="CMD命令:").pack(anchor="w")
        self.cmd_entry = tk.Entry(self.frame, width=80)
        self.cmd_entry.pack(fill="x", pady=(0, 10))
        self.cmd_entry.insert(0, default_cmd)

        self.drop_label = tk.Label(
            self.frame,
            text="把目录拖到这里",
            relief="groove",
            bg="#f0f0f0",
            width=60,
            height=6
        )
        self.drop_label.pack(fill="both", expand=True)

        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.on_drop)

    def on_drop(self, event):
        raw_data = event.data.strip()
        self.log(f"[{self.frame['text']}] 收到拖拽数据: {raw_data}")

        try:
            paths = self.root.tk.splitlist(raw_data)
        except Exception:
            paths = [raw_data]

        paths = [os.path.normpath(path) for path in paths]
        self.log(f"[{self.frame['text']}] 解析后的路径列表: {paths}")

        if not paths:
            self.log(f"[{self.frame['text']}] 未解析到任何路径")
            messagebox.showerror("错误", "未检测到有效的拖拽路径")
            return

        # 检查是否包含文件
        file_paths = [p for p in paths if os.path.isfile(p)]
        if file_paths:
            self.log(f"[{self.frame['text']}] 错误：拖入内容包含文件: {file_paths}")
            messagebox.showerror(
                "错误",
                "拖入内容中包含文件，不支持文件，只能拖入目录。\n\n" + "\n".join(file_paths)
            )
            return

        # 检查是否都是目录
        invalid_paths = [p for p in paths if not os.path.isdir(p)]
        if invalid_paths:
            self.log(f"[{self.frame['text']}] 错误：以下路径不是有效目录: {invalid_paths}")
            messagebox.showerror(
                "错误",
                "以下路径不是有效目录：\n\n" + "\n".join(invalid_paths)
            )
            return

        self.log(f"[{self.frame['text']}] 有效目录列表: {paths}")

        cmd = self.cmd_entry.get().strip()
        self.log(f"[{self.frame['text']}] 输入命令: {cmd}")

        if not cmd:
            self.log(f"[{self.frame['text']}] 错误：CMD命令为空")
            messagebox.showerror("错误", "CMD命令不能为空")
            return

        # 对每个目录分别打开一个 cmd 窗口
        for path in paths:
            self.run_in_cmd(path, cmd)

    def run_in_cmd(self, directory, cmd):
        full_cmd = f'pushd "{directory}" && {cmd}'
        self.log(f"[{self.frame['text']}] 即将执行: {full_cmd}")

        try:
            launch_cmd = f'start "" cmd /k "{full_cmd}"'
            self.log(f"[{self.frame['text']}] 启动命令: {launch_cmd}")

            subprocess.Popen(launch_cmd, shell=True)
            self.log(f"[{self.frame['text']}] 已打开新的 cmd 窗口: {directory}")
        except Exception as e:
            self.log(f"[{self.frame['text']}] 执行失败: {e}")
            messagebox.showerror("执行失败", str(e))


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Maven 拖拽执行工具")
        self.root.geometry("850x600")

        container = tk.Frame(root, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        self.group1 = CommandDropGroup(
            container,
            "第一组",
            "mvn clean install package -o",
            self.write_log,
            root
        )
        self.group1.frame.pack(fill="x", pady=(0, 10))

        self.group2 = CommandDropGroup(
            container,
            "第二组",
            "mvn clean package -o",
            self.write_log,
            root
        )
        self.group2.frame.pack(fill="x", pady=(0, 10))

        tk.Label(container, text="日志输出:").pack(anchor="w", pady=(10, 0))

        self.log_text = ScrolledText(container, height=14, state="disabled")
        self.log_text.pack(fill="both", expand=True, pady=(5, 0))

    def write_log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()
