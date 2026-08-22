@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or not on PATH.
    echo Install Python 3.10+ and try again.
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if exist "requirements.txt" (
    echo.
    echo Dependencies installed successfully.
) else (
    echo.
    echo No requirements.txt found; project uses the standard library only.
)

echo.
echo Setup complete. Run start.bat to launch the app.
pause
