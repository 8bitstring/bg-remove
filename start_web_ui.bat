@echo off
title Local Background Remover - Web UI
echo ===================================================
echo Starting Local Background Remover Web UI...
echo ===================================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python app.py
pause
