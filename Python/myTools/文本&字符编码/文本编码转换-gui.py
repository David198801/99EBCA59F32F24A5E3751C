import os
import sys
import shlex
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# 尝试导入拖放支持，若无则降级为无拖放
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False
    # 使用普通 Tk 类
    TkinterDnD = None
    DND_FILES = None

# 常用编码列表
ENCODINGS = [
    'UTF-8', 'GBK', 'GB2312', 'GB18030', 'Big5', 'ASCII',
    'ISO-8859-1', 'Windows-1252', 'UTF-16', 'UTF-32'
]


class ConvertThread(threading.Thread):
    """转换线程"""
    def __init__(self, file_path, src_enc, dst_enc, buffer_size=1024*1024):
        super().__init__()
        self.file_path = file_path
        self.src_enc = src_enc
        self.dst_enc = dst_enc
        self.buffer_size = buffer_size
        self._cancelled = False
        self.progress = 0          # 0-100
        self.success = False
        self.message = ""

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            base, ext = os.path.splitext(self.file_path)
            out_path = f"{base}_converted{ext}"
            total_size = os.path.getsize(self.file_path)
            processed = 0

            with open(self.file_path, 'r', encoding=self.src_enc, errors='replace') as infile:
                with open(out_path, 'w', encoding=self.dst_enc, errors='replace') as outfile:
                    while True:
                        if self._cancelled:
                            outfile.close()
                            os.remove(out_path)
                            self.message = "转换已取消"
                            return
                        chunk = infile.read(self.buffer_size)
                        if not chunk:
                            break
                        outfile.write(chunk)
                        # 计算进度（近似）
                        processed += len(chunk.encode(self.src_enc, errors='replace'))
                        if total_size > 0:
                            self.progress = int((processed / total_size) * 100)
                        else:
                            self.progress = 50  # 空文件直接给50%

            self.success = True
            self.message = f"转换完成：{out_path}"
            self.progress = 100
        except Exception as e:
            self.success = False
            self.message = f"错误：{str(e)}"


class MainApp(TkinterDnD.Tk if HAS_DND else tk.Tk):
    def __init__(self):
        # 根据是否有DND选择父类
        if HAS_DND:
            super().__init__()
        else:
            tk.Tk.__init__(self)
        self.title("文本编码转换工具")
        self.geometry("600x450")
        self.configure(bg='#f0f0f0')

        # 变量
        self.file_list = []          # 待转换文件路径列表
        self.current_index = 0
        self.convert_thread = None
        self.is_converting = False

        # 创建界面
        self.create_widgets()

        # 如果有DND，注册窗口拖放
        if HAS_DND:
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.on_drop)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # 编码选择
        frame_enc = tk.Frame(self, bg='#f0f0f0')
        frame_enc.pack(pady=5, fill='x', padx=10)

        tk.Label(frame_enc, text="源编码：", bg='#f0f0f0').grid(row=0, column=0, padx=2)
        self.src_var = tk.StringVar(value="UTF-8")
        self.src_combo = ttk.Combobox(frame_enc, textvariable=self.src_var, values=ENCODINGS, width=12)
        self.src_combo.grid(row=0, column=1, padx=5)

        tk.Label(frame_enc, text="目标编码：", bg='#f0f0f0').grid(row=0, column=2, padx=2)
        self.dst_var = tk.StringVar(value="GBK")
        self.dst_combo = ttk.Combobox(frame_enc, textvariable=self.dst_var, values=ENCODINGS, width=12)
        self.dst_combo.grid(row=0, column=3, padx=5)

        # 按钮行
        frame_btn = tk.Frame(self, bg='#f0f0f0')
        frame_btn.pack(pady=5, fill='x', padx=10)

        self.btn_add = tk.Button(frame_btn, text="添加文件", command=self.add_files, width=10)
        self.btn_add.pack(side='left', padx=2)

        self.btn_clear = tk.Button(frame_btn, text="清空列表", command=self.clear_files, width=10)
        self.btn_clear.pack(side='left', padx=2)

        self.btn_convert = tk.Button(frame_btn, text="开始转换", command=self.start_conversion, width=10)
        self.btn_convert.pack(side='left', padx=2)

        self.btn_cancel = tk.Button(frame_btn, text="取消", command=self.cancel_conversion, width=10, state='disabled')
        self.btn_cancel.pack(side='left', padx=2)

        # 文件列表框
        self.listbox = tk.Listbox(self, selectmode='extended', height=12)
        self.listbox.pack(pady=5, padx=10, fill='both', expand=True)

        # 如果支持拖放，为Listbox也注册
        if HAS_DND:
            self.listbox.drop_target_register(DND_FILES)
            self.listbox.dnd_bind('<<Drop>>', self.on_drop_listbox)

        # 进度条
        self.progress = ttk.Progressbar(self, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(pady=5, padx=10, fill='x')

        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        lbl_status = tk.Label(self, textvariable=self.status_var, bg='#f0f0f0', anchor='w')
        lbl_status.pack(pady=5, padx=10, fill='x')

        # 提示
        hint_text = "提示：可拖拽文件到窗口或文件列表区域" if HAS_DND else "提示：使用“添加文件”按钮选择文件"
        hint = tk.Label(self, text=hint_text, bg='#f0f0f0', fg='#666')
        hint.pack(pady=2)

    # ---------- 拖放事件 ----------
    def on_drop(self, event):
        files = self.parse_dnd_data(event.data)
        if files:
            self.add_files_to_list(files)

    def on_drop_listbox(self, event):
        files = self.parse_dnd_data(event.data)
        if files:
            self.add_files_to_list(files)

    def parse_dnd_data(self, data):
        """解析DND返回的字符串，返回文件路径列表"""
        if not isinstance(data, str):
            return []
        # 使用 shlex 处理花括号和空格
        try:
            parts = shlex.split(data)
        except Exception:
            parts = data.split()
        # 过滤存在的文件
        return [p for p in parts if os.path.exists(p)]

    # ---------- 文件操作 ----------
    def add_files(self):
        files = filedialog.askopenfilenames(title="选择文件")
        if files:
            self.add_files_to_list(files)

    def add_files_to_list(self, files):
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
                self.listbox.insert(tk.END, f)
        self.status_var.set(f"已添加 {len(files)} 个文件")

    def clear_files(self):
        self.file_list.clear()
        self.listbox.delete(0, tk.END)
        self.progress['value'] = 0
        self.status_var.set("已清空列表")

    # ---------- 转换控制 ----------
    def start_conversion(self):
        if not self.file_list:
            messagebox.showwarning("警告", "没有待转换的文件！")
            return

        src = self.src_var.get()
        dst = self.dst_var.get()
        if src == dst:
            if not messagebox.askyesno("确认", "源编码和目标编码相同，确定继续？"):
                return

        self.is_converting = True
        self.set_ui_enabled(False)
        self.progress['value'] = 0
        self.current_index = 0
        self.status_var.set("正在转换...")
        self.convert_next()

    def convert_next(self):
        if self.current_index >= len(self.file_list):
            self.finish_conversion(True, "所有文件转换完成！")
            return

        file_path = self.file_list[self.current_index]
        self.status_var.set(f"正在转换：{os.path.basename(file_path)}")
        src = self.src_var.get()
        dst = self.dst_var.get()

        self.convert_thread = ConvertThread(file_path, src, dst)
        self.convert_thread.start()
        self.check_thread()  # 开始轮询线程状态

    def check_thread(self):
        if self.convert_thread and self.convert_thread.is_alive():
            # 更新进度
            self.progress['value'] = self.convert_thread.progress
            self.after(100, self.check_thread)
        else:
            # 线程结束
            if self.convert_thread:
                success = self.convert_thread.success
                msg = self.convert_thread.message
                if success:
                    self.current_index += 1
                    self.status_var.set(msg)
                    self.progress['value'] = 100
                    # 继续下一个
                    self.after(0, self.convert_next)
                else:
                    # 出错或取消
                    self.finish_conversion(False, msg)
            else:
                self.finish_conversion(False, "未知错误")

    def finish_conversion(self, success, msg):
        self.is_converting = False
        self.set_ui_enabled(True)
        if not success:
            messagebox.showerror("转换失败", msg)
            self.progress['value'] = 0
        else:
            self.progress['value'] = 100
            self.status_var.set(msg)
        self.convert_thread = None

    def cancel_conversion(self):
        if self.convert_thread and self.convert_thread.is_alive():
            self.convert_thread.cancel()
            self.status_var.set("正在取消...")
            self.btn_cancel.config(state='disabled')
            # 等待线程结束（在check_thread中处理）
        else:
            self.is_converting = False
            self.set_ui_enabled(True)

    def set_ui_enabled(self, enabled):
        """启用/禁用界面元素"""
        state = 'normal' if enabled else 'disabled'
        self.src_combo.config(state=state)
        self.dst_combo.config(state=state)
        # 按钮
        self.btn_add.config(state=state)
        self.btn_clear.config(state=state)
        self.btn_convert.config(state=state)
        self.btn_cancel.config(state='disabled' if enabled else 'normal')

    def on_close(self):
        # 如果正在转换，尝试取消
        if self.is_converting and self.convert_thread and self.convert_thread.is_alive():
            self.convert_thread.cancel()
            self.convert_thread.join(1.0)
        self.destroy()


if __name__ == "__main__":
    if not HAS_DND:
        # 弹出警告，但程序仍可运行（无拖拽功能）
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "缺少拖放支持",
            "未安装 tkinterdnd2，拖放功能不可用。\n您仍可通过“添加文件”按钮选择文件。\n\n如需拖放，请运行：\npip install tkinterdnd2"
        )
        root.destroy()

    app = MainApp()
    app.mainloop()