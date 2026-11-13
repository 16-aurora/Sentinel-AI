@echo off
title Sentinel AI - REST API

echo ==========================================
echo       SENTINEL AI - REST API V1
echo ==========================================
echo.

call "%~dp0.venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Could not activate the virtual environment.
    pause
    exit /b 1
)

echo Starting Sentinel AI API...
echo.
echo API: http://127.0.0.1:8000
echo Interactive documentation: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop the server.
echo.

python -m uvicorn main:app --reload --app-dir "%~dp0src\api" --host 127.0.0.1 --port 8000

pause
