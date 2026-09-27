@echo off
title Remove Background - Drop Image Here
cd /d "%~dp0"

if "%~1"=="" (
    echo.
    echo [!] Drag and drop an image file onto this .bat file to remove its background.
    echo.
    pause
    exit /b
)

echo Removing background from: "%~nx1"
call .venv\Scripts\activate.bat
python remove_bg.py "%~1"
echo.
echo Process finished!
pause
