# Implementation Roadmap

## Phase 1 — Architecture & Scaffolding ✅ done
- Complete folder structure (frontend/backend/shared/docs/scripts/assets/config/tests).
- Service interfaces defined (no implementations).
- Tooling configs (Vite, Tailwind, tsconfig, pyproject/requirements, ESLint/Ruff).
- `.env.example` files, README, architecture/API docs.
- CI skeleton (lint/type-check only, no deploy).

## Phase 2a — Backend Infrastructure ✅ done
- FastAPI app factory with lifespan (startup/shutdown logging, DI container construction).
- `Settings` fully implemented with validation (`app.core.config`).
- Structured JSON logging, console + rotating file handler (`app.core.logging`).
- Full middleware stack: request id, timing, CORS, trusted hosts, GZip, security headers, error
  logging (`app.middleware`).
- Global exception handling → unified `{success, error: {code, message, details}}` envelope
  (`app.middleware.error_handler`).
- Root health/liveness/version endpoints — live, no external calls (`health_routes.py`).
- Versioned resource routers wired to DI, returning `501 Not Implemented`.
- Placeholder implementations for all 8 services + DI container/providers.
- pytest configured; tests for health, version, startup, and config validation.

## Phase 3 — Frontend (mock data) ✅ done
- Premium ChatGPT-style UI: Landing, Research, Settings, 404 pages.
- Zustand state, theme system (light/dark/system, persisted), Framer Motion animations.
- AI Growth Opportunities™ cards, mock research pipeline simulation.
- No backend integration yet — everything runs on mock data (see `frontend/src/utils/mockData/`).

## Phase 4 — Real AI Research Pipeline ✅ done (this phase)
- `SearchService` (`SerperSearchService`) — real Serper.dev integration, retry/timeout/error
  handling via the shared `AsyncHttpClient`.
- `CompanyService` (`DefaultCompanyService`) — name/URL resolution; URLs skip search entirely.
- `CrawlerService` (`Crawl4AICrawlerService`) — real Crawl4AI integration, seed-path + internal-link
  discovery, capped at 10 pages, concurrent fetches, graceful degradation on failure.
- Content preprocessing (`app.utils.text_cleaning`) — dedup, cookie-banner stripping, ~12,000-word cap.
- `AIService` (`OpenRouterAIService`) — real OpenRouter integration, one structured call per
  research run, model selectable per-request.
- `CompetitorService` / `OpportunityService` (`AICompetitorService`, `AIOpportunityService`) — real,
  independently callable implementations (not used by the main pipeline, which derives both from its
  single combined AI call — see `research_report_service.py`).
- `ReportService` (`ResearchReportService`) — the real orchestrator: resolve → search → crawl →
  extract → **one** AI call → map → return. In-memory report cache (no DB yet).
- `POST /api/v1/research` / `GET /api/v1/research/{id}` — live, validated, structured-error-handling
  endpoints.
- Tests: Serper client, OpenRouter client, AI service (prompt rendering + JSON parsing), research
  endpoint (mocked service, no real network calls).
- **Not done this phase**: frontend wired to this real endpoint (frontend still uses mock data —
  Phase 3's mock pipeline and this phase's real pipeline currently exist in parallel, not connected).

## Phase 5 — Frontend Integration
- Replace `frontend/src/hooks/useConversationStore.ts`'s mock simulation with real calls to
  `POST /api/v1/research`.
- Wire `ModelSelector` to send the selected model id in the request.
- Loading/error states for real network latency and failures (including `status: "failed"` partial
  results).

## Phase 6 — Reporting Enhancements
- PDF generation (`pdf/`) with ReportLab: cover, summary, competitors, opportunities sections.
- Async job handling for long-running report generation (status polling) — `/research` is currently
  synchronous.
- Dedicated standalone routes for `company`, `report`, `opportunities` (currently reached only via
  the combined `/research` pipeline).

## Phase 7 — Discord Delivery
- Implement `DiscordService` + webhook/bot integration.
- Frontend: "Send to Discord" action + delivery confirmation.

## Phase 8 — Hardening & Launch
- Rate limiting / abuse protection on paid upstream calls (Serper/OpenRouter cost money per request).
- Persistent storage for companies/reports (currently in-memory, lost on restart).
- Full logging/observability review.
- E2E tests (Playwright) across the full flow.
- Deploy: Vercel (frontend) + Render (backend), CORS lockdown, production env review.
- Operational note: Crawl4AI requires a one-time `playwright install chromium` (or
  `python -m playwright install chromium`) after `pip install -r requirements.txt` — the Python
  package alone does not include the browser binary.
- Architecture Decision Records finalized for: async job strategy, auth (if added), error budget.

---

Each phase should only touch files inside folders already reserved for it in
[ARCHITECTURE.md](ARCHITECTURE.md) — no phase should require restructuring the tree.
