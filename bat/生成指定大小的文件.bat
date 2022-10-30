@echo off
set filename=%random%.txt
set size=300
rem µ¥Î»MB
set /a sizeMB=%size%*1024*1024
fsutil file createnew %filename% %sizeMB%