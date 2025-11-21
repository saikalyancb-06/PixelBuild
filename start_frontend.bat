@echo off
cd /d "%~dp0frontend"
set PORT=3001
echo Starting Frontend Server...
npm start
pause
