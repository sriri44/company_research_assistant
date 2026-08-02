#!/usr/bin/env bash
# Bootstraps both apps for local development on macOS/Linux/CI.
# Usage: bash scripts/setup.sh
set -euo pipefail

echo "Setting up backend..."
cd backend
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
cd ..

echo "Setting up frontend..."
cd frontend
npm install
[ -f .env ] || cp .env.example .env
cd ..

echo "Done. Fill in real API keys in backend/.env and frontend/.env before running."
