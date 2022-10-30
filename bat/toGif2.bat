@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
for  %%i in (*) do (
  set str=%%~xi
  if not !str! ==.bat (ffmpeg -i "%%i" -b 100k "%%i.gif"
  )
)
pause