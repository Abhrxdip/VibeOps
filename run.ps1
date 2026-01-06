Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   MailMind - Neural Email Intelligence" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $PSScriptRoot

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Install Python 3.8+" -ForegroundColor Red
    exit 1
}

try {
    python -c "import streamlit" 2>$null
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

if (-Not (Test-Path ".env")) {
    if (Test-Path "config\.env.example") {
        Write-Host "Creating .env file..." -ForegroundColor Yellow
        Copy-Item "config\.env.example" ".env"
        Write-Host "✓ Created .env - Edit if needed" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Starting MailMind..." -ForegroundColor Cyan
Write-Host "Default URL: http://localhost:8501" -ForegroundColor Gray
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

streamlit run src/app.py
