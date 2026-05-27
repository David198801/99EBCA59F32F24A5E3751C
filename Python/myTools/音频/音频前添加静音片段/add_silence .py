#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shlex

# ========== 这里直接修改参数 ==========

INPUT_FILE = "input.mp3"          # 输入音频文件
OUTPUT_FILE = "output.mp3"        # 输出音频文件
SILENCE_HOURS = 2                 # 前置静音时长（小时，可写小数，如 1.5）
SAMPLE_RATE = 44100               # 静音采样率
CHANNELS = 2                      # 声道数：1=mono, 2=stereo
FFMPEG_BIN = "ffmpeg"             # ffmpeg 可执行文件路径

# ====================================


def run_cmd(cmd):
    print("执行命令：")
    print(" ".join(shlex.quote(str(x)) for x in cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"命令执行失败，返回码: {result.returncode}")


def main():
    if not os.path.isfile(INPUT_FILE):
        print(f"错误：输入文件不存在: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    if SILENCE_HOURS < 0:
        print("错误：静音时长不能为负数", file=sys.stderr)
        sys.exit(1)

    silence_seconds = SILENCE_HOURS * 3600

    channel_layout = "stereo" if CHANNELS == 2 else "mono"

    cmd = [
        FFMPEG_BIN,
        "-y",
        "-f", "lavfi",
        "-t", str(silence_seconds),
        "-i", f"anullsrc=r={SAMPLE_RATE}:cl={channel_layout}",
        "-i", INPUT_FILE,
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
        "-map", "[outa]",
        OUTPUT_FILE
    ]

    try:
        run_cmd(cmd)
        print(f"\n处理完成，输出文件：{OUTPUT_FILE}")
    except Exception as e:
        print(f"处理失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()