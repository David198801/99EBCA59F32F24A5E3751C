@echo off
for  %%i in (*.ts) do (
  if not "%%i"=="%~nx0" (ffmpeg -i "%%i" -c copy "%%~ni.mp4"
  rem ffmpeg -i "%%i" -r 8 -s 640x480 -t 3 -ss 00:00:00 "%%i.gif"
  rem 不改分辨率反而更小
  )
)