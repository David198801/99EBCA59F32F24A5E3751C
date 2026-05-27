import os
import subprocess
import tkinter as tk
from tkinter import messagebox

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    raise ImportError("请先安装 tkinterdnd2：pip install tkinterdnd2")


class VideoClipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FFmpeg 视频剪辑工具")
        self.root.geometry("680x360")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f7f7")

        self.video_path = tk.StringVar()
        self.start_time = tk.StringVar()
        self.end_time = tk.StringVar()

        # 全局字体设置为微软雅黑 UI
        self.default_font = ("Microsoft YaHei UI", 10)
        self.title_font = ("Microsoft YaHei UI", 12, "bold")
        self.button_font = ("Microsoft YaHei UI", 11, "bold")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="拖入视频文件后，输入起始和结束时间进行剪辑",
            font=self.title_font,
            bg="#f7f7f7"
        )
        title_label.pack(pady=12)

        # 拖拽区域
        self.drop_frame = tk.Label(
            self.root,
            text="将视频文件拖到这里",
            relief="groove",
            width=70,
            height=5,
            bg="#ffffff",
            font=self.default_font
        )
        self.drop_frame.pack(pady=10)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self.drop_file)

        # 文件路径显示
        file_frame = tk.Frame(self.root, bg="#f7f7f7")
        file_frame.pack(fill="x", padx=20, pady=8)

        tk.Label(file_frame, text="文件路径：", font=self.default_font, bg="#f7f7f7").pack(side="left")
        self.file_entry = tk.Entry(file_frame, textvariable=self.video_path, width=72, font=self.default_font)
        self.file_entry.pack(side="left", padx=5)

        # 起始时间
        start_frame = tk.Frame(self.root, bg="#f7f7f7")
        start_frame.pack(fill="x", padx=20, pady=8)
        tk.Label(start_frame, text="起始时间：", font=self.default_font, bg="#f7f7f7").pack(side="left")
        tk.Entry(start_frame, textvariable=self.start_time, width=20, font=self.default_font).pack(side="left", padx=5)
        tk.Label(start_frame, text="格式如：00:00:10 或 10", font=self.default_font, bg="#f7f7f7").pack(side="left")

        # 结束时间
        end_frame = tk.Frame(self.root, bg="#f7f7f7")
        end_frame.pack(fill="x", padx=20, pady=8)
        tk.Label(end_frame, text="结束时间：", font=self.default_font, bg="#f7f7f7").pack(side="left")
        tk.Entry(end_frame, textvariable=self.end_time, width=20, font=self.default_font).pack(side="left", padx=5)
        tk.Label(end_frame, text="格式如：00:01:30 或 90", font=self.default_font, bg="#f7f7f7").pack(side="left")

        # 执行按钮
        self.run_button = tk.Button(
            self.root,
            text="执行剪辑",
            command=self.run_ffmpeg,
            width=18,
            height=2,
            bg="#2d89ef",
            fg="white",
            activebackground="#1b6fc2",
            activeforeground="white",
            font=self.button_font,
            relief="flat",
            cursor="hand2"
        )
        self.run_button.pack(pady=22)

    def drop_file(self, event):
        file_path = event.data.strip()

        # 处理 Windows 下拖入路径带大括号的情况
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]

        if os.path.isfile(file_path):
            self.video_path.set(file_path)
        else:
            messagebox.showerror("错误", "拖入的不是有效文件")

    def run_ffmpeg(self):
        input_file = self.video_path.get().strip()
        start = self.start_time.get().strip()
        end = self.end_time.get().strip()

        if not input_file:
            messagebox.showerror("错误", "请先拖入视频文件")
            return

        if not os.path.isfile(input_file):
            messagebox.showerror("错误", "视频文件不存在")
            return

        if not start and not end:
            messagebox.showerror("错误", "起始时间和结束时间至少填写一个")
            return

        input_dir = os.path.dirname(input_file)
        input_name = os.path.basename(input_file)
        name, ext = os.path.splitext(input_name)

        output_dir = os.path.join(input_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, f"{name}_clip{ext}")

        cmd = ["ffmpeg", "-y"]

        if start:
            cmd.extend(["-ss", start])

        cmd.extend(["-i", input_file])

        if end:
            cmd.extend(["-to", end])

        cmd.extend(["-c", "copy", output_file])

        try:
            self.run_button.config(state="disabled", text="处理中...")
            self.root.update()

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            self.run_button.config(state="normal", text="执行剪辑")

            if result.returncode == 0:
                messagebox.showinfo("成功", f"剪辑完成！\n输出文件：\n{output_file}")
            else:
                messagebox.showerror("FFmpeg 执行失败", result.stderr)

        except FileNotFoundError:
            self.run_button.config(state="normal", text="执行剪辑")
            messagebox.showerror("错误", "未找到 ffmpeg，请先安装 ffmpeg 并加入环境变量")
        except Exception as e:
            self.run_button.config(state="normal", text="执行剪辑")
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = VideoClipApp(root)
    root.mainloop()