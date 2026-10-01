@echo off
title SondeR AI Office - Master Services Launcher
cd /d "%~dp0"
echo ======================================================
echo   SondeR AI Office & Telegram Bot Master Launcher
echo   Pimpinan: Nor Anisa, S.Kom., M.Kom.
echo ======================================================
echo.
echo [1/2] Menjalankan SondeR AI Office Server (Port 19845)...
start "SondeR AI Office 3D" /min python ai_office_server.py
echo [2/2] Menjalankan Telegram Bot Service (@noranisa_bot)...
start "SondeR Telegram Bot" python telegram_bot.py
echo.
echo ======================================================
echo   Semua service aktif!
echo   - AI Office 3D: http://127.0.0.1:19845/
echo   - Telegram Bot: https://t.me/noranisa_bot
echo ======================================================
timeout /t 5
