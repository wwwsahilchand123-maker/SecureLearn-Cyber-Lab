@echo off
title SecureLearn Cyber Lab

cd /d "%~dp0"

echo ==========================================
echo       SecureLearn Cyber Lab
echo ==========================================
echo.
echo Starting Flask server...
echo.

if exist "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

python run_server.py
pause