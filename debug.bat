@echo off
title Neko Cat debug
set "DEST=%LOCALAPPDATA%\SondeRcat"
if exist "%DEST%\sondercat\nekocat.py" (
  py -3 "%DEST%\sondercat\nekocat.py" 2>nul || python "%DEST%\sondercat\nekocat.py"
) else (
  py -3 "%~dp0nekocat.py" 2>nul || python "%~dp0nekocat.py"
)
echo.
echo (any error above is what to screenshot)
pause
