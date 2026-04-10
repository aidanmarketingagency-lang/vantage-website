@echo off
title Vantage — Frontend (React)

echo ============================================================
echo  Vantage Frontend — React 19 + Tailwind
echo ============================================================
echo.

cd /d "%~dp0frontend"

:: Use Node from NVM install
set NODE_PATH=C:\Users\aidan\AppData\Local\nvm\v24.14.1
set PATH=%NODE_PATH%;%PATH%

if not exist "%NODE_PATH%\node.exe" (
    echo ERROR: Node.js not found at %NODE_PATH%
    echo Install Node.js from https://nodejs.org or update this script.
    pause
    exit /b 1
)

:: Check .env exists
if not exist ".env" (
    echo ERROR: frontend\.env not found.
    echo Create frontend\.env with REACT_APP_BACKEND_URL=http://localhost:8001
    pause
    exit /b 1
)

:: Check node_modules
if not exist "node_modules" (
    echo node_modules not found — running npm install...
    npm install --legacy-peer-deps
    echo.
)

echo Starting React dev server on http://localhost:3000 ...
echo Press Ctrl+C to stop.
echo.

npm start

pause
