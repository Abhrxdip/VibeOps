@echo off

echo ==================================
echo   MailMind - Setup and Launch
echo ==================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

echo Checking .env file...
if not exist ".env" (
    echo Creating .env from template...
    copy "config\.env.example" ".env" >nul
    echo [OK] Created .env file
    echo Note: Edit .env to add your API keys (optional for mock mode)
) else (
    echo [OK] .env file already exists
)
echo.

echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

echo ==================================
echo   Starting MailMind...
echo ==================================
echo.
echo The app will open in your browser automatically
echo Default mode: Mock Data (no API keys required)
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run src/app.py
