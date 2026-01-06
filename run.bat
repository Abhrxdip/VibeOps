@echo off
echo.
echo ==========================================
echo   MailMind - Neural Email Intelligence
echo ==========================================
echo.

cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

if not exist ".env" (
    if exist "config\.env.example" (
        echo Creating .env file...
        copy "config\.env.example" ".env" >nul
        echo [OK] Created .env - Edit if needed
    )
)

echo.
echo Starting MailMind...
echo Default URL: http://localhost:8501
echo Press Ctrl+C to stop
echo.

streamlit run src/app.py

pause
