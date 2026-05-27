@echo off
for  %%i in (*) do (
  if not "%%i"=="%~nx0" (ffmpeg -i "%%i" -vn -acodec libfdk_aac -profile:a aac_he -vbr 5 "%%~ni.m4a"
  )
)