@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
  start "" ".venv\Scripts\pythonw.exe" "nekocat.py"
) else (
  where py >nul 2>nul && (py nekocat.py) || (python nekocat.py)
)
