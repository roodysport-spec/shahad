@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo =======================================================
echo   SHM LOAD Platform v2.0
echo   Starting Backend and Frontend servers...
echo =======================================================
echo.

taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im node.exe /t >nul 2>&1

echo [1/3] Starting Backend (port 8000)...
start "SHM-Backend" cmd /c "chcp 65001 >nul && cd /d "%~dp0" && py -3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

echo [2/3] Starting Frontend (port 5173)...
start "SHM-Frontend" cmd /c "chcp 65001 >nul && cd /d "%~dp0frontend" && npm run dev -- --host 127.0.0.1 --port 5173"

echo [3/3] Opening browser in 4 seconds...
ping 127.0.0.1 -n 5 >nul
start "" "http://localhost:5173"

echo.
echo =======================================================
echo   SHM LOAD is now running at: http://localhost:5173
echo   Keep this window open or minimize it.
echo =======================================================
echo.
pause