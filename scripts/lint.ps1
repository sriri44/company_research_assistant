# Runs linters/formatters/type-checkers for both apps.
# Usage: powershell -File scripts/lint.ps1

Write-Host "Linting backend..."
Set-Location backend
ruff check .
black --check .
mypy app
Set-Location ..

Write-Host "Linting frontend..."
Set-Location frontend
npm run lint
Set-Location ..
