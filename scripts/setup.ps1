# Bootstraps both apps for local development on Windows.
# Usage: powershell -File scripts/setup.ps1

Write-Host "Setting up backend..."
Set-Location backend
if (-not (Test-Path ".venv")) { python -m venv .venv }
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Set-Location ..

Write-Host "Setting up frontend..."
Set-Location frontend
npm install
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
Set-Location ..

Write-Host "Done. Fill in real API keys in backend/.env and frontend/.env before running."
