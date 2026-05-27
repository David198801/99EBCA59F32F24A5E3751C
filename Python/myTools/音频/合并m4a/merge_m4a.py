import os
import sys
import subprocess
from pathlib import Path


def get_audio_channels(file_path: Path):
    """
    使用 ffprobe 获取音频声道数
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=channels",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        return int(output) if output.isdigit() else None
    except Exception:
        return None


def main():
    script_dir = Path(__file__).resolve().parent
    output_file = script_dir / "merged.m4a"
    concat_file = script_dir / "ffmpeg_concat_list.txt"

    # 获取当前目录下所有 m4a 文件，并按字符串顺序排序
    m4a_files = sorted(
        [f for f in script_dir.iterdir() if f.is_file() and f.suffix.lower() == ".m4a"],
        key=lambda x: x.name
    )

    # 排除输出文件本身
    m4a_files = [f for f in m4a_files if f.name != output_file.name]

    if not m4a_files:
        print("当前目录下没有找到 m4a 文件。")
        sys.exit(1)

    print("检测音频声道信息：")
    need_reencode = False

    for f in m4a_files:
        channels = get_audio_channels(f)
        if channels is None:
            print(f"  {f.name}: 无法获取声道数，默认将重编码处理")
            need_reencode = True
        else:
            print(f"  {f.name}: {channels} 声道")
            if channels > 2:
                need_reencode = True

    # 生成 concat 列表
    with open(concat_file, "w", encoding="utf-8") as f:
        for file in m4a_files:
            file_path = file.resolve().as_posix().replace("'", r"'\''")
            f.write(f"file '{file_path}'\n")

    if need_reencode:
        print("\n检测到多声道音频（或无法检测的音频），将统一重编码为 2 声道 AAC 后合并。")
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-ac", "2",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_file)
        ]
    else:
        print("\n所有音频均为 1~2 声道，直接复制音频流合并。")
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(output_file)
        ]

    print("\n将要合并以下文件：")
    for f in m4a_files:
        print(f"  {f.name}")

    print(f"\n输出文件：{output_file.name}")
    print("正在调用 ffmpeg...")

    try:
        subprocess.run(cmd, check=True)
        print("合并完成。")
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg 执行失败：{e}")
        sys.exit(1)
    finally:
        if concat_file.exists():
            concat_file.unlink()


if __name__ == "__main__":
    main()