@echo off
cd /d "%~dp0backend"
set PYTHONPATH=%~dp0
echo Starting Backend Server...
python main.py
pause
