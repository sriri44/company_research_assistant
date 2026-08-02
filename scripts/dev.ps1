# Runs backend and frontend dev servers concurrently in separate windows.
# Usage: powershell -File scripts/dev.ps1

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .venv/Scripts/Activate.ps1; uvicorn app.main:app --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
