@echo off
for  %%i in (*) do (
  if not "%%i"=="%~nx0" (ffmpeg -i "%%i"  -ab 256k "%%~ni.m4a"
  )
)