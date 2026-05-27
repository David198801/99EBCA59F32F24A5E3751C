@echo off
for  %%i in (*) do (
  if not "%%i"=="%~nx0" (ffmpeg -i "%%i" -vn -acodec libfdk_aac -profile:a aac_he -ar 44100 -ab 320k "%%~ni.m4a"
  )
)