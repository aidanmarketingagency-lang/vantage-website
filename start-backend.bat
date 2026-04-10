@echo off
title Vantage — Backend (FastAPI)

echo ============================================================
echo  Vantage Backend — FastAPI + MongoDB
echo ============================================================
echo.

cd /d "%~dp0backend"

:: Use Python 3.11 from the known install path
set PYTHON=C:\Users\aidan\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PYTHON%" (
    echo ERROR: Python 3.11 not found at %PYTHON%
    echo Please install Python 3.11 or update this script.
    pause
    exit /b 1
)

:: Check .env exists
if not exist ".env" (
    echo ERROR: backend\.env not found.
    echo Copy backend\.env and fill in MONGO_URL, JWT_SECRET, etc.
    pause
    exit /b 1
)

echo Starting uvicorn on http://localhost:8001 ...
echo Press Ctrl+C to stop.
echo.

"%PYTHON%" -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload

pause
