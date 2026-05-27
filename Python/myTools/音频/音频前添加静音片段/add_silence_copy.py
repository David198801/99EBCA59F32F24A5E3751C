#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import tempfile
import subprocess
import shlex

# ========== 硬编码参数 ==========
INPUT_FILE = "摩登家庭2.m4a"         # 输入音频文件
OUTPUT_FILE = "摩登家庭21.m4a"       # 输出音频文件
SILENCE_HOURS = 5               # 静音时长（小时，可小数）
FFMPEG_BIN = "ffmpeg"
FFPROBE_BIN = "ffprobe"
# =================================


def run_cmd(cmd, capture_output=False, text=True):
    print("执行命令：")
    print(" ".join(shlex.quote(str(x)) for x in cmd))
    return subprocess.run(
        cmd,
        check=False,
        capture_output=capture_output,
        text=text
    )


def probe_audio_info(input_file):
    cmd = [
        FFPROBE_BIN,
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,channel_layout,bit_rate",
        "-of", "json",
        input_file
    ]
    result = run_cmd(cmd, capture_output=True)

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe 执行失败：\n{result.stderr}")

    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    if not streams:
        raise RuntimeError("没有找到音频流")

    stream = streams[0]

    codec_name = stream.get("codec_name")
    sample_rate = int(stream["sample_rate"]) if stream.get("sample_rate") else 44100
    channels = int(stream["channels"]) if stream.get("channels") else 2
    channel_layout = stream.get("channel_layout")
    bit_rate = stream.get("bit_rate")
    if bit_rate is not None:
        try:
            bit_rate = int(bit_rate)
        except ValueError:
            bit_rate = None

    return {
        "codec_name": codec_name,
        "sample_rate": sample_rate,
        "channels": channels,
        "channel_layout": channel_layout,
        "bit_rate": bit_rate,
    }


def get_extension(path):
    return os.path.splitext(path)[1].lower()


def choose_channel_layout(channels, channel_layout):
    if channel_layout:
        return channel_layout

    mapping = {
        1: "mono",
        2: "stereo",
        6: "5.1",
        8: "7.1",
    }
    return mapping.get(channels, "stereo")


def build_silence_encode_cmd(info, silence_seconds, silence_file):
    codec = info["codec_name"]
    sample_rate = info["sample_rate"]
    channels = info["channels"]
    channel_layout = choose_channel_layout(channels, info["channel_layout"])
    bit_rate = info["bit_rate"]

    input_src = f"anullsrc=r={sample_rate}:cl={channel_layout}"

    cmd = [
        FFMPEG_BIN,
        "-y",
        "-f", "lavfi",
        "-t", str(silence_seconds),
        "-i", input_src,
    ]

    if codec == "mp3":
        cmd += ["-c:a", "libmp3lame"]
        if bit_rate:
            cmd += ["-b:a", str(bit_rate)]
        cmd += ["-ar", str(sample_rate), "-ac", str(channels), silence_file]

    elif codec == "aac":
        cmd += ["-c:a", "aac"]
        if bit_rate:
            cmd += ["-b:a", str(bit_rate)]
        cmd += ["-ar", str(sample_rate), "-ac", str(channels), silence_file]

    elif codec == "flac":
        cmd += ["-c:a", "flac", "-ar", str(sample_rate), "-ac", str(channels), silence_file]

    elif codec in ("wav", "pcm_s16le"):
        cmd += ["-c:a", "pcm_s16le", "-ar", str(sample_rate), "-ac", str(channels), silence_file]

    else:
        raise RuntimeError(
            f"暂不支持针对 codec={codec} 做安全的流复制拼接。\n"
            f"建议改为重编码 concat 方案。"
        )

    return cmd


def ffconcat_escape(path):
    # ffmpeg concat demuxer 列表中的单引号转义
    return os.path.abspath(path).replace("'", r"'\''")


def main():
    if not os.path.isfile(INPUT_FILE):
        print(f"错误：输入文件不存在: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    if SILENCE_HOURS < 0:
        print("错误：静音时长不能为负数", file=sys.stderr)
        sys.exit(1)

    silence_seconds = SILENCE_HOURS * 3600

    try:
        info = probe_audio_info(INPUT_FILE)
        print("检测到原音频参数：")
        print(json.dumps(info, indent=2, ensure_ascii=False))

        input_ext = get_extension(INPUT_FILE)
        output_ext = get_extension(OUTPUT_FILE)

        if input_ext != output_ext:
            raise RuntimeError(
                f"输入输出扩展名不一致：{input_ext} != {output_ext}\n"
                f"流复制拼接通常要求容器格式一致。"
            )

        with tempfile.TemporaryDirectory() as tmpdir:
            silence_file = os.path.join(tmpdir, f"silence{input_ext}")
            list_file = os.path.join(tmpdir, "concat_list.txt")

            # 1. 生成静音文件
            cmd1 = build_silence_encode_cmd(info, silence_seconds, silence_file)
            result1 = run_cmd(cmd1)
            if result1.returncode != 0:
                raise RuntimeError("静音文件生成失败")

            # 2. 写 concat 列表
            silence_path = ffconcat_escape(silence_file)
            input_path = ffconcat_escape(INPUT_FILE)
            with open(list_file, "w", encoding="utf-8") as f:
                f.write(f"file '{silence_path}'\n")
                f.write(f"file '{input_path}'\n")

            # 3. 流复制拼接
            cmd2 = [
                FFMPEG_BIN,
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c", "copy",
                OUTPUT_FILE
            ]
            result2 = run_cmd(cmd2)
            if result2.returncode != 0:
                raise RuntimeError("音频合并失败")

        print(f"\n处理完成，输出文件：{OUTPUT_FILE}")

    except Exception as e:
        print(f"处理失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()