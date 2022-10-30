@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
for  %%i in (*) do (
  set str=%%i
  if not !str:~-4! ==.bat (ffmpeg -i "!str!" -b 100k "!str!.gif"
  )
)
pause