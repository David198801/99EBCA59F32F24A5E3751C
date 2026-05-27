@echo off
for  %%i in (*.dff) do (
  if not "%%i"=="%~nx0" (ffmpeg -i "%%i" -ar 88200 "%%~ni.flac"
  )
)