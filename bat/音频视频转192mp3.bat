@echo off
for  %%i in (*) do (
  if not "%%i"=="%~nx0" (ffmpeg -i "%%i" -vn -ab 192k "%%~ni.mp3"
  )
)