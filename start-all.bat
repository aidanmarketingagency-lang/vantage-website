@echo off
title Vantage — Full Stack

echo ============================================================
echo  Vantage — Starting Backend + Frontend
echo ============================================================
echo.

:: Launch backend in its own window
start "Vantage Backend" cmd /k "%~dp0start-backend.bat"

:: Small delay so backend gets a head start
timeout /t 3 /nobreak >nul

:: Launch frontend in its own window
start "Vantage Frontend" cmd /k "%~dp0start-frontend.bat"

echo.
echo Both servers are starting in separate windows.
echo   Backend:  http://localhost:8001
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8001/docs
echo.
