@echo off
setlocal

set TOMCAT_HOME=D:\TOMCAT\apache-tomcat-9.0.68
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_351

cd /d %TOMCAT_HOME%\bin

rem 先正常关闭
call shutdown.bat

rem 等 10 秒
timeout /t 10 /nobreak >nul

rem 如果 8080 端口还在，就强杀
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080') do (
    taskkill /PID %%a /F >nul 2>nul
)

rem 再等 90 秒
timeout /t 90 /nobreak >nul

rem 启动
call startup.bat

endlocal