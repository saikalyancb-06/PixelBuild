@echo off
echo ========================================
echo   FAKE APP DETECTION SYSTEM
echo ========================================
echo.
echo Starting Backend and Frontend servers...
echo.

start "Backend Server" cmd /k "%~dp0start_backend.bat"
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "%~dp0start_frontend.bat"

echo.
echo Both servers are starting in separate windows.
echo.
echo Backend will run on: http://localhost:8000
echo Frontend will run on: http://localhost:3001
echo.
echo Open http://localhost:3001 in your browser
echo.
pause
