import os
import json
import math
import subprocess

# =========================
# 硬编码输入输出路径
# =========================
INPUT_FILE = r"D:\Downloads\bili\格局.mp4"
OUTPUT_DIR = r"segments"
SEGMENT_SECONDS = 10

# 是否关闭音频：
# False = 保留音频（默认）
# True  = 不输出音频
DISABLE_AUDIO = True


def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("命令执行失败：")
        print(" ".join(cmd))
        print(result.stderr)
        raise RuntimeError("命令执行失败")
    return result.stdout


def get_video_info(input_file):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=avg_frame_rate,r_frame_rate,nb_frames,duration",
        "-show_entries", "format=duration",
        "-of", "json",
        input_file
    ]
    output = run_cmd(cmd)
    data = json.loads(output)

    stream = data["streams"][0]
    fmt = data.get("format", {})

    avg_frame_rate = stream.get("avg_frame_rate", "0/0")
    r_frame_rate = stream.get("r_frame_rate", "0/0")
    nb_frames = stream.get("nb_frames")
    duration = stream.get("duration") or fmt.get("duration")

    return {
        "avg_frame_rate": avg_frame_rate,
        "r_frame_rate": r_frame_rate,
        "nb_frames": nb_frames,
        "duration": float(duration) if duration else None
    }


def has_audio_stream(input_file):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=index",
        "-of", "csv=p=0",
        input_file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return bool(result.stdout.strip())


def parse_fraction(frac_str):
    if not frac_str or frac_str == "0/0":
        return 0.0
    num, den = frac_str.split("/")
    num = float(num)
    den = float(den)
    if den == 0:
        return 0.0
    return num / den


def get_exact_total_frames(input_file):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-count_frames",
        "-show_entries", "stream=nb_read_frames",
        "-of", "default=nokey=1:noprint_wrappers=1",
        input_file
    ]
    output = run_cmd(cmd).strip()
    return int(output)


def split_by_frames(input_file, output_dir, segment_seconds, disable_audio=False):
    os.makedirs(output_dir, exist_ok=True)

    info = get_video_info(input_file)

    fps = parse_fraction(info["avg_frame_rate"])
    if fps <= 0:
        fps = parse_fraction(info["r_frame_rate"])

    if fps <= 0:
        raise ValueError("无法获取视频帧率")

    print(f"检测到 FPS: {fps}")

    try:
        total_frames = get_exact_total_frames(input_file)
        print(f"精确统计总帧数: {total_frames}")
    except Exception:
        if info["nb_frames"] and str(info["nb_frames"]).isdigit():
            total_frames = int(info["nb_frames"])
            print(f"使用 nb_frames 总帧数: {total_frames}")
        elif info["duration"]:
            total_frames = int(round(info["duration"] * fps))
            print(f"使用 duration * fps 估算总帧数: {total_frames}")
        else:
            raise ValueError("无法获取总帧数")

    frames_per_segment = int(round(segment_seconds * fps))
    if frames_per_segment <= 0:
        raise ValueError("每段帧数计算失败")

    print(f"每 {segment_seconds} 秒对应帧数: {frames_per_segment}")

    num_segments = math.ceil(total_frames / frames_per_segment)
    print(f"预计分割段数: {num_segments}")

    audio_exists = has_audio_stream(input_file)
    print(f"检测到音频流: {audio_exists}")
    print(f"关闭音频选项 disable_audio: {disable_audio}")

    for i in range(num_segments):
        start_frame = i * frames_per_segment
        end_frame = min((i + 1) * frames_per_segment, total_frames)

        start_time = start_frame / fps
        end_time = end_frame / fps

        output_file = os.path.join(output_dir, f"segment_{i:03d}.mp4")

        print(f"\n正在导出第 {i} 段:")
        print(f"  起始帧: {start_frame}")
        print(f"  结束帧: {end_frame}")
        print(f"  起始时间: {start_time:.6f}")
        print(f"  结束时间: {end_time:.6f}")
        print(f"  输出文件: {output_file}")

        # 根据是否关闭音频，构造不同 ffmpeg 命令
        if disable_audio or not audio_exists:
            cmd = [
                "ffmpeg",
                "-y",
                "-i", input_file,
                "-filter_complex",
                f"[0:v]trim=start={start_time}:end={end_time},setpts=PTS-STARTPTS[v]",
                "-map", "[v]",
                "-an",
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "18",
                output_file
            ]
        else:
            cmd = [
                "ffmpeg",
                "-y",
                "-i", input_file,
                "-filter_complex",
                (
                    f"[0:v]trim=start={start_time}:end={end_time},setpts=PTS-STARTPTS[v];"
                    f"[0:a]atrim=start={start_time}:end={end_time},asetpts=PTS-STARTPTS[a]"
                ),
                "-map", "[v]",
                "-map", "[a]",
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "18",
                "-c:a", "aac",
                "-b:a", "192k",
                output_file
            ]

        subprocess.run(cmd, check=True)

    print("\n分割完成。")


if __name__ == "__main__":
    split_by_frames(INPUT_FILE, OUTPUT_DIR, SEGMENT_SECONDS, disable_audio=DISABLE_AUDIO)
