@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist "output" mkdir "output"

for %%F in (*.mp4) do (
    echo 正在处理: %%F
    ffmpeg -y -i "%%F" -to 00:13:14 -c copy "output\%%~nF.mp4"
)

echo 处理完成
pause