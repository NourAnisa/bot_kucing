@echo off
title Neko Cat - one click install
echo.
echo    /\_/\     Neko Cat
echo   ( o.o )    Setting everything up for you...
echo.
if exist "%~dp0install.bat" (
    call "%~dp0install.bat"
    goto :eof
)
for /d %%D in ("%~dp0*") do (
    if exist "%%D\install.bat" (
        call "%%D\install.bat"
        goto :eof
    )
)
echo [!] Couldn't find install.bat next to this file or in a subfolder.
echo     Make sure you extracted the WHOLE zip, then run this again.
pause
