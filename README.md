# AI Company Research Assistant

Enter a company name or website URL and get back an AI-generated research report: company summary,
competitor analysis, and **AI Growth Opportunities™** — automation ideas ranked by business impact,
implementation complexity, and priority.

> **Status**: Phase 4 — the real AI research pipeline is live. `POST /api/v1/research` runs
> resolve → search (Serper.dev) → crawl (Crawl4AI) → extract → **one** AI call (OpenRouter) →
> competitors → AI Growth Opportunities™ end to end. The frontend still runs on mock data (not yet
> wired to this endpoint — see [docs/ROADMAP.md](docs/ROADMAP.md) Phase 5).

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, TypeScript, TailwindCSS, shadcn/ui, Framer Motion |
| Backend | FastAPI, Python 3.12+ |
| AI | OpenRouter |
| Search | Serper.dev |
| Crawler | Crawl4AI |
| PDF | ReportLab |
| Deployment | Vercel (frontend) · Render (backend) |

## Project Structure

```
company-research-assistant/
├── frontend/     # React SPA
├── backend/      # FastAPI service
├── shared/       # Cross-language contract references
├── docs/         # Architecture, API design, roadmap, ADRs
├── scripts/      # Dev/setup scripts
├── assets/       # Branding & design assets
├── config/       # Environment templates
└── tests/        # Cross-cutting e2e/integration tests
```

Full rationale for every folder: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — folder structure, service interfaces, data flow, conventions
- [API Design](docs/API_DESIGN.md) — endpoint map and contract shapes
- [Coding Standards](docs/CODING_STANDARDS.md) — naming, review checklist
- [Roadmap](docs/ROADMAP.md) — phased implementation plan

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.12+ (developed/tested against 3.10+; see `backend/pyproject.toml`)
- API keys: [Serper.dev](https://serper.dev/api-key) and [OpenRouter](https://openrouter.ai/keys) —
  required for real research results (the app boots and responds without them, but resolution/AI
  calls will fail with a clear error)

### Setup

```bash
# Backend
cd backend
cp .env.example .env      # then fill in SERPER_API_KEY and OPENROUTER_API_KEY
python -m venv .venv
.venv/Scripts/activate     # Windows — use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
python -m playwright install chromium   # one-time: Crawl4AI's browser binary (not installed by pip)

# Frontend
cd frontend
cp .env.example .env
npm install
```

Or run `scripts/setup.ps1` (Windows) / `scripts/setup.sh` (macOS/Linux/CI) to do all of the above
(the Playwright browser install is still a separate manual step).

### Running locally

```bash
# Backend — http://localhost:8000, interactive docs at /docs
cd backend && .venv/Scripts/activate && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

Or `scripts/dev.ps1` to launch both in separate terminal windows.

### Verifying the backend is up

```bash
curl http://localhost:8000/health
curl http://localhost:8000/version

# Real research pipeline (needs SERPER_API_KEY + OPENROUTER_API_KEY configured):
curl -X POST http://localhost:8000/api/v1/research \
  -H "Content-Type: application/json" \
  -d '{"query": "stripe.com"}'
```

### Developer workflow

1. Make changes inside the existing folder structure (docs/ARCHITECTURE.md is the source of truth —
   don't add new top-level folders or move files between layers).
2. Run linters/type-checks: `scripts/lint.ps1`, or manually — `ruff check .`, `black --check .`,
   `mypy app` from `backend/`; `npm run lint` from `frontend/`.
3. Run backend tests: `pytest` from `backend/` (see [Testing](#testing) below).
4. Update the matching doc (`docs/API_DESIGN.md`, `docs/ARCHITECTURE.md`) if you changed a contract,
   per the review checklist in [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md).

### Testing

```bash
cd backend && .venv/Scripts/activate && pytest
```

Coverage: root health/version/readiness endpoints, app startup (lifespan), configuration
loading/validation, the Serper/OpenRouter clients and AI service (all with mocked HTTP — no real
network calls in the test suite), and the `/api/v1/research` endpoint (mocked service layer).

## Environment Variables

Backend (`backend/.env.example`): `APP_NAME`, `APP_VERSION`, `APP_ENV`, `DEBUG`, `HOST`, `PORT`,
`API_PREFIX`, `CORS_ALLOWED_ORIGINS`, `ALLOWED_HOSTS`, `SERPER_API_KEY`, `SERPER_BASE_URL`,
`OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `OPENROUTER_DEFAULT_MODEL`, `DISCORD_TOKEN`,
`DISCORD_CHANNEL`, `LOG_LEVEL`, `PDF_OUTPUT_PATH`, `MAX_CRAWL_PAGES`, `REQUEST_TIMEOUT`,
`USER_AGENT`, `HTTP_MAX_RETRIES`, `HTTP_RETRY_BACKOFF_SECONDS`, `AI_REQUEST_TIMEOUT`,
`MAX_CONTEXT_WORDS`. All are validated by `app.core.config.Settings` at startup — an invalid
`LOG_LEVEL` or `APP_ENV`, or an out-of-range `PORT`, fails fast with a clear error instead of
booting into a bad state.

Frontend (`frontend/.env.example`): `VITE_API_BASE_URL`.

Never commit real `.env` files — only `.env.example` templates.

## License

TBD.
