@echo off
for %%f in (*.*) do (
    if not "%%~nf"=="%~n0" ren "%%f" "%%~nf.rar"
)