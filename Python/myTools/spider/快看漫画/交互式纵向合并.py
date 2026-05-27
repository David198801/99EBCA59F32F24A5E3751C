import os
import shutil
from pathlib import Path
from PIL import Image
from tkinter import Label
from tkinterdnd2 import TkinterDnD, DND_FILES


SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff"}


def get_next_merge_filename(folder: Path) -> Path:
    index = 1
    while True:
        candidate = folder / f"merge_{index:03d}.png"
        if not candidate.exists():
            return candidate
        index += 1


def parse_dropped_files(data: str):
    files = []
    current = ""
    in_brace = False

    for ch in data:
        if ch == "{":
            in_brace = True
            current = ""
        elif ch == "}":
            in_brace = False
            files.append(current)
            current = ""
        elif ch == " " and not in_brace:
            if current:
                files.append(current)
                current = ""
        else:
            current += ch

    if current:
        files.append(current)

    return [f.strip() for f in files if f.strip()]


def validate_files(file_paths):
    if not file_paths:
        raise ValueError("未检测到拖入的文件。")

    paths = [Path(p) for p in file_paths]

    for p in paths:
        if not p.exists():
            raise ValueError(f"文件不存在：{p}")
        if not p.is_file():
            raise ValueError(f"不是文件：{p}")
        if p.suffix.lower() not in SUPPORTED_EXTS:
            raise ValueError(f"不支持的图片格式：{p.name}")

    parent_dirs = {p.parent.resolve() for p in paths}
    if len(parent_dirs) != 1:
        raise ValueError("请仅拖入同一目录下的图片。")

    return paths


def merge_images_vertically(image_paths, output_path: Path):
    images = []
    try:
        for p in image_paths:
            img = Image.open(p).convert("RGBA")
            images.append(img)

        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)

        merged = Image.new("RGBA", (max_width, total_height), (255, 255, 255, 0))

        y = 0
        for img in images:
            merged.paste(img, (0, y))
            y += img.height

        merged.save(output_path, "PNG")

    finally:
        for img in images:
            try:
                img.close()
            except:
                pass


def move_to_origin(image_paths, source_dir: Path):
    origin_dir = source_dir / "origin"
    origin_dir.mkdir(exist_ok=True)

    for p in image_paths:
        target = origin_dir / p.name

        if target.exists():
            stem = p.stem
            suffix = p.suffix
            index = 1
            while True:
                new_target = origin_dir / f"{stem}_{index:03d}{suffix}"
                if not new_target.exists():
                    target = new_target
                    break
                index += 1

        shutil.move(str(p), str(target))


def handle_drop(event, label: Label):
    try:
        dropped_files = parse_dropped_files(event.data)
        image_paths = validate_files(dropped_files)

        image_paths = sorted(image_paths, key=lambda p: p.name)

        source_dir = image_paths[0].parent
        output_path = get_next_merge_filename(source_dir)

        merge_images_vertically(image_paths, output_path)
        move_to_origin(image_paths, source_dir)

        label.config(
            text=(
                "合并完成！\n\n"
                f"输出文件：{output_path.name}\n"
                f"原图已移动到：{source_dir / 'origin'}\n\n"
                "可继续拖入下一组图片"
            )
        )

    except Exception as e:
        label.config(
            text=(
                "处理失败，请重新拖入图片。\n\n"
                f"错误信息：{e}"
            )
        )


def main():
    root = TkinterDnD.Tk()
    root.title("纵向合并图片")
    root.geometry("520x260")
    root.resizable(False, False)

    label = Label(
        root,
        text="把同一目录下的多张图片拖到这里\n\n将按文件名字典序排序后纵向合并\n输出为 merge_001.png，并把原图移到 origin 目录",
        width=60,
        height=12,
        relief="groove",
        justify="center",
        font=("Arial", 11)
    )
    label.pack(padx=20, pady=30, fill="both", expand=True)

    label.drop_target_register(DND_FILES)
    label.dnd_bind("<<Drop>>", lambda event: handle_drop(event, label))

    root.mainloop()


if __name__ == "__main__":
    main()