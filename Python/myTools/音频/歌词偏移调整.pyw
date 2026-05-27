import os
import re
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from tkinterdnd2 import DND_FILES, TkinterDnD
from mutagen.id3 import ID3, USLT, SYLT, ID3NoHeaderError
from mutagen.flac import FLAC
from mutagen.mp4 import MP4


AUDIO_EXTS = {".mp3", ".flac", ".m4a"}
LRC_EXTS = {".lrc"}

META_TAG_PATTERN = re.compile(r'^\[(ar|ti|al|by|offset|re|ve):.*\]$', re.IGNORECASE)
TIME_TAG_PATTERN = re.compile(r'\[(\d{1,3}):(\d{1,2})(?:\.(\d{1,3}))?\]')


class LyricOffsetTool:
    def __init__(self, root):
        self.root = root
        self.root.title("歌词整体偏移调整工具 - 增强版")
        self.root.geometry("920x650")

        self.current_file = None
        self.current_type = None  # lrc/mp3/flac/m4a
        self.original_content = None
        self.preview_content = None

        # 锁定行：保存“原始文本中的行号（从0开始）”
        self.locked_lines = set()

        # 自动备份开关
        self.auto_backup_var = tk.BooleanVar(value=False)

        self.build_ui()

    def build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="文件:").pack(side="left")
        self.file_var = tk.StringVar(value="未载入")
        ttk.Entry(top, textvariable=self.file_var, state="readonly").pack(
            side="left", fill="x", expand=True, padx=5
        )
        ttk.Button(top, text="选择文件", command=self.select_file).pack(side="left", padx=5)

        offset_frame = ttk.Frame(self.root, padding=(10, 0))
        offset_frame.pack(fill="x")

        ttk.Label(offset_frame, text="偏移量(毫秒，可正可负):").pack(side="left")
        self.offset_var = tk.StringVar(value="0")
        ttk.Entry(offset_frame, textvariable=self.offset_var, width=12).pack(side="left", padx=5)

        ttk.Button(offset_frame, text="预览偏移", command=self.preview_offset).pack(side="left", padx=5)
        ttk.Button(offset_frame, text="保存到原文件", command=self.save_file).pack(side="left", padx=5)
        ttk.Button(offset_frame, text="另存为 LRC", command=self.save_as_lrc).pack(side="left", padx=5)
        ttk.Button(offset_frame, text="重新载入", command=self.reload_current_file).pack(side="left", padx=5)

        # 自动备份勾选框
        ttk.Checkbutton(
            offset_frame,
            text="保存前自动备份(.bak)",
            variable=self.auto_backup_var
        ).pack(side="left", padx=10)

        drag_frame = ttk.LabelFrame(self.root, text="拖拽区", padding=10)
        drag_frame.pack(fill="x", padx=10, pady=5)

        self.drop_area = tk.Text(drag_frame, height=4)
        self.drop_area.pack(fill="x")
        self.drop_area.insert("1.0", "把 .lrc / .mp3 / .flac / .m4a 文件拖到这里\n")
        self.drop_area.config(state="disabled")

        main_pane = ttk.PanedWindow(self.root, orient="horizontal")
        main_pane.pack(fill="both", expand=True, padx=10, pady=5)

        # 左侧：歌词预览
        left_frame = ttk.LabelFrame(main_pane, text="歌词预览 / 选择行后可锁定", padding=5)
        main_pane.add(left_frame, weight=4)

        self.text = tk.Text(left_frame, wrap="none", undo=False)
        self.text.pack(side="left", fill="both", expand=True)

        yscroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.text.yview)
        yscroll.pack(side="right", fill="y")
        self.text.config(yscrollcommand=yscroll.set)

        self.text.tag_configure("locked", background="#fff2a8")
        self.text.tag_configure("meta", foreground="#6666aa")
        self.text.tag_configure("changed", foreground="#006400")

        # 右侧：锁定控制
        right_frame = ttk.LabelFrame(main_pane, text="锁定控制", padding=8)
        main_pane.add(right_frame, weight=1)

        ttk.Label(
            right_frame,
            text="用法：\n1. 在左侧文本框选中若干行\n2. 点击“锁定选中行”\n3. 偏移时这些行保持不变",
            justify="left"
        ).pack(anchor="w", pady=(0, 8))

        ttk.Button(right_frame, text="锁定选中行", command=self.lock_selected_lines).pack(fill="x", pady=2)
        ttk.Button(right_frame, text="解锁选中行", command=self.unlock_selected_lines).pack(fill="x", pady=2)
        ttk.Button(right_frame, text="清空全部锁定", command=self.clear_locked_lines).pack(fill="x", pady=2)

        ttk.Label(right_frame, text="已锁定行号:").pack(anchor="w", pady=(10, 2))
        self.locked_list = tk.Listbox(right_frame, height=18)
        self.locked_list.pack(fill="both", expand=True)

        bottom = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        bottom.pack(fill="x")

        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(bottom, textvariable=self.status_var).pack(anchor="w")

        # 拖拽
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

    # ---------------- UI 基础 ----------------

    def set_status(self, text):
        self.status_var.set(text)

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="选择歌词或音频文件",
            filetypes=[
                ("支持的文件", "*.lrc *.mp3 *.flac *.m4a"),
                ("LRC", "*.lrc"),
                ("MP3", "*.mp3"),
                ("FLAC", "*.flac"),
                ("M4A", "*.m4a"),
                ("所有文件", "*.*"),
            ]
        )
        if filepath:
            self.load_file(filepath)

    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if not files:
            return
        filepath = files[0]
        self.load_file(filepath)

    def reload_current_file(self):
        if not self.current_file:
            messagebox.showinfo("提示", "当前没有文件")
            return
        self.load_file(self.current_file)

    # ---------------- 文件读写 ----------------

    def load_file(self, filepath):
        if not os.path.isfile(filepath):
            messagebox.showerror("错误", "文件不存在")
            return

        ext = os.path.splitext(filepath)[1].lower()

        try:
            if ext in LRC_EXTS:
                self.current_type = "lrc"
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            elif ext == ".mp3":
                self.current_type = "mp3"
                content = self.read_mp3_lyrics(filepath)
            elif ext == ".flac":
                self.current_type = "flac"
                content = self.read_flac_lyrics(filepath)
            elif ext == ".m4a":
                self.current_type = "m4a"
                content = self.read_m4a_lyrics(filepath)
            else:
                messagebox.showerror("错误", f"不支持的文件类型: {ext}")
                return

            self.current_file = filepath
            self.file_var.set(filepath)
            self.original_content = content
            self.preview_content = content
            self.locked_lines.clear()

            self.refresh_text(content)
            self.refresh_locked_list()
            self.apply_line_styles()

            self.set_status("已载入文件")

        except UnicodeDecodeError:
            messagebox.showerror("读取失败", "LRC 文件编码不是 UTF-8，可自行扩展为自动检测编码")
        except Exception as e:
            messagebox.showerror("读取失败", str(e))

    def backup_file(self, filepath):
        backup_path = filepath + ".bak"
        shutil.copy2(filepath, backup_path)
        return backup_path

    def save_file(self):
        if not self.current_file or self.original_content is None:
            messagebox.showwarning("提示", "请先载入文件")
            return

        try:
            offset_ms = self.parse_offset_ms()
            new_content = self.apply_offset_with_locks(self.original_content, offset_ms, self.locked_lines)

            backup_path = None
            if self.auto_backup_var.get():
                backup_path = self.backup_file(self.current_file)

            if self.current_type == "lrc":
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(new_content)

            elif self.current_type == "mp3":
                self.write_mp3_lyrics(self.current_file, new_content)

            elif self.current_type == "flac":
                self.write_flac_lyrics(self.current_file, new_content)

            elif self.current_type == "m4a":
                self.write_m4a_lyrics(self.current_file, new_content)

            self.original_content = new_content
            self.preview_content = new_content
            self.refresh_text(new_content)
            self.apply_line_styles()

            if backup_path:
                self.set_status(f"已保存到原文件，并已备份: {backup_path}")
                messagebox.showinfo("成功", f"已保存到原文件\n并创建备份文件：\n{backup_path}")
            else:
                self.set_status("已保存到原文件（未备份）")
                messagebox.showinfo("成功", "已保存到原文件\n未创建备份文件")

        except Exception as e:
            messagebox.showerror("保存失败", str(e))

    def save_as_lrc(self):
        if self.original_content is None:
            messagebox.showwarning("提示", "请先载入文件")
            return

        try:
            offset_ms = self.parse_offset_ms()
            new_content = self.apply_offset_with_locks(self.original_content, offset_ms, self.locked_lines)

            default_name = "output.lrc"
            if self.current_file:
                base = os.path.splitext(os.path.basename(self.current_file))[0]
                default_name = f"{base}.lrc"

            save_path = filedialog.asksaveasfilename(
                title="另存为 LRC",
                defaultextension=".lrc",
                initialfile=default_name,
                filetypes=[("LRC 文件", "*.lrc"), ("所有文件", "*.*")]
            )
            if not save_path:
                return

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            self.preview_content = new_content
            self.refresh_text(new_content)
            self.apply_line_styles()
            self.set_status(f"已另存为 LRC: {save_path}")
            messagebox.showinfo("成功", f"已另存为 LRC:\n{save_path}")

        except Exception as e:
            messagebox.showerror("另存失败", str(e))

    # ---------------- 预览与偏移 ----------------

    def parse_offset_ms(self):
        try:
            return int(self.offset_var.get().strip())
        except ValueError:
            raise ValueError("偏移量必须是整数毫秒")

    def preview_offset(self):
        if self.original_content is None:
            messagebox.showwarning("提示", "请先载入文件")
            return

        try:
            offset_ms = self.parse_offset_ms()
            new_content = self.apply_offset_with_locks(self.original_content, offset_ms, self.locked_lines)
            self.preview_content = new_content
            self.refresh_text(new_content)
            self.apply_line_styles(compare_to_original=True)
            self.set_status("已生成预览")
        except Exception as e:
            messagebox.showerror("预览失败", str(e))

    def apply_offset_with_locks(self, content, offset_ms, locked_lines):
        lines = content.splitlines()
        out_lines = []

        for idx, line in enumerate(lines):
            if idx in locked_lines:
                out_lines.append(line)
                continue

            # 元标签不改
            if META_TAG_PATTERN.match(line.strip()):
                out_lines.append(line)
                continue

            out_lines.append(self.apply_offset_to_line(line, offset_ms))

        return "\n".join(out_lines)

    def apply_offset_to_line(self, line, offset_ms):
        matches = list(TIME_TAG_PATTERN.finditer(line))
        if not matches:
            return line

        new_line = line
        replacements = []

        for m in matches:
            mm = int(m.group(1))
            ss = int(m.group(2))
            frac = m.group(3) or "0"

            if len(frac) == 1:
                ms = int(frac) * 100
            elif len(frac) == 2:
                ms = int(frac) * 10
            else:
                ms = int(frac[:3])

            total_ms = (mm * 60 + ss) * 1000 + ms + offset_ms
            if total_ms < 0:
                total_ms = 0

            new_mm = total_ms // 60000
            rem = total_ms % 60000
            new_ss = rem // 1000
            new_ms = rem % 1000

            # 输出 [mm:ss.xx]
            new_tag = f"[{new_mm:02d}:{new_ss:02d}.{new_ms // 10:02d}]"
            replacements.append((m.span(), new_tag))

        for span, new_tag in reversed(replacements):
            start, end = span
            new_line = new_line[:start] + new_tag + new_line[end:]

        return new_line

    # ---------------- 锁定行 ----------------

    def get_selected_line_range(self):
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")
        except tk.TclError:
            return None

        start_line = int(start.split(".")[0]) - 1
        end_line = int(end.split(".")[0]) - 1
        return start_line, end_line

    def lock_selected_lines(self):
        line_range = self.get_selected_line_range()
        if line_range is None:
            messagebox.showinfo("提示", "请先在左侧预览框中选中一些行")
            return

        start_line, end_line = line_range
        for i in range(start_line, end_line + 1):
            self.locked_lines.add(i)

        self.refresh_locked_list()
        self.apply_line_styles()
        self.set_status(f"已锁定 {start_line + 1}~{end_line + 1} 行")

    def unlock_selected_lines(self):
        line_range = self.get_selected_line_range()
        if line_range is None:
            messagebox.showinfo("提示", "请先在左侧预览框中选中一些行")
            return

        start_line, end_line = line_range
        for i in range(start_line, end_line + 1):
            self.locked_lines.discard(i)

        self.refresh_locked_list()
        self.apply_line_styles()
        self.set_status(f"已解锁 {start_line + 1}~{end_line + 1} 行")

    def clear_locked_lines(self):
        self.locked_lines.clear()
        self.refresh_locked_list()
        self.apply_line_styles()
        self.set_status("已清空全部锁定")

    def refresh_locked_list(self):
        self.locked_list.delete(0, tk.END)
        for line_no in sorted(self.locked_lines):
            self.locked_list.insert(tk.END, f"第 {line_no + 1} 行")

    # ---------------- 文本显示 ----------------

    def refresh_text(self, content):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content if content else "[未找到歌词内容]")

    def apply_line_styles(self, compare_to_original=False):
        self.text.tag_remove("locked", "1.0", tk.END)
        self.text.tag_remove("meta", "1.0", tk.END)
        self.text.tag_remove("changed", "1.0", tk.END)

        current_lines = self.text.get("1.0", "end-1c").splitlines()
        original_lines = self.original_content.splitlines() if self.original_content else []

        for i, line in enumerate(current_lines):
            start = f"{i + 1}.0"
            end = f"{i + 1}.end"

            if i in self.locked_lines:
                self.text.tag_add("locked", start, end)

            if META_TAG_PATTERN.match(line.strip()):
                self.text.tag_add("meta", start, end)

            if compare_to_original:
                if i < len(original_lines) and line != original_lines[i]:
                    self.text.tag_add("changed", start, end)

    # ---------------- MP3 / FLAC / M4A ----------------

    def read_mp3_lyrics(self, filepath):
        try:
            tags = ID3(filepath)
        except ID3NoHeaderError:
            raise Exception("MP3 文件没有 ID3 标签")

        sylt_list = tags.getall("SYLT")
        if sylt_list:
            sylt = sylt_list[0]
            lines = []
            for text, timestamp in sylt.text:
                total_ms = int(timestamp)
                mm = total_ms // 60000
                rem = total_ms % 60000
                ss = rem // 1000
                ms = rem % 1000
                lines.append(f"[{mm:02d}:{ss:02d}.{ms // 10:02d}]{text}")
            return "\n".join(lines)

        uslt_list = tags.getall("USLT")
        if uslt_list:
            return uslt_list[0].text

        raise Exception("MP3 中未找到歌词标签（USLT/SYLT）")

    def write_mp3_lyrics(self, filepath, lyric_text):
        try:
            tags = ID3(filepath)
        except ID3NoHeaderError:
            tags = ID3()

        sylt_list = tags.getall("SYLT")
        if sylt_list:
            tags.delall("SYLT")
            sylt_data = self.lrc_to_sylt(lyric_text)
            tags.add(SYLT(encoding=3, lang="eng", format=2, type=1, text=sylt_data))
        else:
            tags.delall("USLT")
            tags.add(USLT(encoding=3, lang="eng", desc="", text=lyric_text))

        tags.save(filepath)

    def lrc_to_sylt(self, lyric_text):
        result = []

        # 支持一行多个时间标签
        for line in lyric_text.splitlines():
            tags = list(TIME_TAG_PATTERN.finditer(line))
            if not tags:
                continue

            lyric_part = TIME_TAG_PATTERN.sub("", line).strip()

            for m in tags:
                mm = int(m.group(1))
                ss = int(m.group(2))
                frac = m.group(3) or "0"

                if len(frac) == 1:
                    ms = int(frac) * 100
                elif len(frac) == 2:
                    ms = int(frac) * 10
                else:
                    ms = int(frac[:3])

                total_ms = (mm * 60 + ss) * 1000 + ms
                result.append((lyric_part, total_ms))

        result.sort(key=lambda x: x[1])
        return result

    def read_flac_lyrics(self, filepath):
        audio = FLAC(filepath)
        if "LYRICS" in audio:
            return "\n".join(audio["LYRICS"])
        if "UNSYNCEDLYRICS" in audio:
            return "\n".join(audio["UNSYNCEDLYRICS"])
        raise Exception("FLAC 中未找到歌词字段（LYRICS/UNSYNCEDLYRICS）")

    def write_flac_lyrics(self, filepath, lyric_text):
        audio = FLAC(filepath)
        if "LYRICS" in audio:
            audio["LYRICS"] = [lyric_text]
        elif "UNSYNCEDLYRICS" in audio:
            audio["UNSYNCEDLYRICS"] = [lyric_text]
        else:
            audio["LYRICS"] = [lyric_text]
        audio.save()

    def read_m4a_lyrics(self, filepath):
        audio = MP4(filepath)
        lyrics = audio.tags.get("\xa9lyr")
        if lyrics:
            return "\n".join(lyrics)
        raise Exception("M4A 中未找到歌词标签（©lyr）")

    def write_m4a_lyrics(self, filepath, lyric_text):
        audio = MP4(filepath)
        if audio.tags is None:
            audio.add_tags()
        audio["\xa9lyr"] = [lyric_text]
        audio.save()


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = LyricOffsetTool(root)
    root.mainloop()