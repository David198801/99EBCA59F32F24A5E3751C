@echo off
setlocal enabledelayedexpansion

:: 创建输出文件夹
set output_dir=converted_wav
if not exist "!output_dir!" (
    mkdir "!output_dir!"
)

:: 转换所有 .wav 文件
for %%f in (*.wav) do (
    ffmpeg -i "%%f" -ar 44100 "!output_dir!\%%~nf_converted.wav"
)

:: 转换所有 .mp3 文件
for %%f in (*.mp3) do (
    ffmpeg -i "%%f" -ar 44100 "!output_dir!\%%~nf_converted.wav"
)

echo 所有文件已成功转换到 "!output_dir!" 文件夹中。
pause