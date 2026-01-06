Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  MailMind - Setup & Launch" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""

if (-Not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "config\.env.example" ".env"
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host "  Note: Edit .env to add your API keys (optional for mock mode)" -ForegroundColor Gray
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Write-Host ""

Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import streamlit" 2>$null
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
} catch {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Starting MailMind..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open in your browser automatically" -ForegroundColor Gray
Write-Host "Default mode: Mock Data (no API keys required)" -ForegroundColor Gray
Write-Host ""

streamlit run src/app.py
