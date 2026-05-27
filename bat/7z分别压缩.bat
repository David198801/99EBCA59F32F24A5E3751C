@echo off
for /d %%i in (*) do (
    echo 正在压缩并删除: "%%i"
    7z a -t7z "%%i.7z" "%%i" -sdel
)
echo 所有操作已完成。
pause