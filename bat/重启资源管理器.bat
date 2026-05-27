@echo off
echo 正在重启 Windows 资源管理器...

taskkill /f /im explorer.exe
timeout /t 2 /nobreak >nul

start "" "%windir%\explorer.exe"

timeout /t 2 /nobreak >nul
tasklist /fi "imagename eq explorer.exe" | find /i "explorer.exe" >nul
if errorlevel 1 (
    echo Explorer 启动失败，正在再次尝试...
    start "" explorer.exe
) else (
    echo Explorer 已重启
)

exit