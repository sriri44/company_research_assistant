# Architecture — AI Company Research Assistant

Status: **Phase 1 — Architecture & Scaffolding**
No business logic, endpoints, crawling, or AI integration is implemented yet. This document is the
source of truth for how the system is organized and why.

---

## 1. System Overview

The AI Company Research Assistant accepts a **company name or website URL** from a user and will
(in later phases) search the web, crawl the company's site, extract structured content, run AI
analysis, identify competitors, surface **AI Growth Opportunities™**, render a PDF report, and
optionally push results to Discord.

Phase 1 goal: build a scaffold so rigorous that Phase 2+ is "fill in the function body," not
"figure out where this goes."

### Guiding principles

- **SOLID** — every service is defined as an interface (protocol/ABC) first; concrete
  implementations are swappable without touching callers.
- **Dependency Injection** — routes and services never instantiate their own dependencies; FastAPI's
  `Depends()` graph (wired in `backend/app/core/container.py`) owns construction.
- **Separation of concerns** — search, crawling, AI, PDF, and Discord are independent bounded
  contexts. None of them import each other directly; they are composed by an orchestrator
  (`ReportService`).
- **Contract-first** — Pydantic schemas (backend) and TypeScript types (frontend) mirror each other
  via `shared/`, so the API contract is never ambiguous.
- **No monoliths** — no file should contain more than one reason to change. A route file only
  wires HTTP → service. A service file only orchestrates. A client file only talks to one
  external API.

---

## 2. Top-Level Layout

```
company-research-assistant/
├── frontend/       # React + Vite + TS SPA
├── backend/        # FastAPI application
├── shared/         # Cross-language contracts (types/constants used by both sides conceptually)
├── docs/           # Architecture, API design, roadmap, ADRs
├── scripts/        # Dev/setup/CI helper scripts
├── assets/         # Branding, screenshots, static design assets (not served by the app)
├── config/         # Environment-specific config templates
├── tests/          # Cross-cutting e2e / integration tests (spans frontend+backend)
└── .github/        # CI workflows
```

Each top-level folder maps to a distinct concern so that CI, deployment, and code owners can target
them independently (e.g., Vercel only needs `frontend/`, Render only needs `backend/`).

---

## 3. Backend — `backend/app/`

FastAPI app, Python 3.12+. Organized as **layered + service-oriented**: HTTP layer never contains
business logic; business logic never imports HTTP concerns.

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/          # HTTP endpoints (thin controllers)
│   │       └── dependencies/    # FastAPI Depends() providers
│   ├── core/                    # config, DI container, exceptions, logging, security
│   ├── services/
│   │   ├── interfaces/          # Abstract service contracts (Protocols/ABCs)
│   │   └── implementations/     # Concrete implementations (Phase 2+)
│   ├── crawler/                 # Crawl4AI integration boundary
│   │   └── strategies/          # Pluggable crawl strategies (static, JS-render, sitemap…)
│   ├── search/                  # Serper.dev integration boundary
│   │   └── providers/           # Pluggable search providers
│   ├── ai/                      # OpenRouter integration boundary
│   │   ├── providers/           # Pluggable model providers
│   │   └── opportunities/       # AI Growth Opportunities™ engine (see §7)
│   ├── pdf/                     # ReportLab report generation
│   │   ├── templates/           # Layout/section definitions
│   │   └── builders/            # Composable PDF section builders
│   ├── discord/                 # Discord webhook/bot integration
│   ├── models/                  # Internal domain models (dataclasses/ORM-agnostic)
│   ├── schemas/                 # Pydantic request/response DTOs (API contract)
│   ├── utils/                   # Pure, stateless helper functions
│   ├── prompts/                 # Versioned AI prompt templates (no business logic)
│   ├── clients/                 # Thin HTTP client wrappers for 3rd-party APIs
│   ├── middleware/               # Cross-cutting request/response middleware
│   └── main.py                  # App factory — assembles routers, middleware, DI
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
├── requirements.txt
└── .env.example
```

### Folder-by-folder responsibilities

| Folder | Why it exists | What belongs here | Responsibility |
|---|---|---|---|
| `api/v1/routes/` | Isolate HTTP concerns from logic so endpoints stay swappable/versionable | One router module per resource: `company_routes.py`, `report_routes.py`, `competitor_routes.py`, `opportunity_routes.py`, `discord_routes.py`, `health_routes.py` | Parse request → call a service via DI → return schema. No business logic, no direct client calls. |
| `api/v1/dependencies/` | Central place for `Depends()` providers so routes stay declarative | `get_search_service.py`, `get_ai_service.py`, `get_current_settings.py`, pagination/query-param dependencies | Wire interfaces to concrete implementations for a given request scope. |
| `core/` | Application-wide concerns that don't belong to any one feature | `config.py` (Settings), `container.py` (DI wiring), `exceptions.py` (domain exceptions), `logging.py`, `constants.py`, `security.py` | Bootstraps the app; owns cross-cutting config/DI/error taxonomy. |
| `services/interfaces/` | SOLID's Dependency Inversion — routes and other services depend on abstractions, never concretions | One `Protocol`/ABC per service (`SearchService`, `CrawlerService`, `AIService`, `ReportService`, `DiscordService`, `CompetitorService`, `CompanyService`, `OpportunityService`) | Define method signatures + docstring contracts only. No implementation. |
| `services/implementations/` | Keeps concrete logic separate from contracts so alt implementations (e.g., a mock for tests, a v2 provider) can coexist | `default_search_service.py`, `default_ai_service.py`, etc. (created in Phase 2) | Implements an interface; orchestrates clients/crawler/ai as needed. |
| `crawler/` | Isolates Crawl4AI so it can be swapped/mocked without touching services | `crawler_client.py` (wraps Crawl4AI), `strategies/*.py` (per-site-type crawl strategy) | Fetch + normalize raw page content. No AI, no persistence. |
| `search/` | Isolates Serper.dev so search providers are pluggable | `serper_client.py`, `providers/*.py` | Resolve a company name/URL to candidate web results. |
| `ai/` | Isolates OpenRouter/model access from prompt content and business use | `openrouter_client.py`, `providers/*.py` | Send prompts, return raw model output. No prompt authoring here. |
| `ai/opportunities/` | Dedicated home for the **AI Growth Opportunities™** engine, kept separate because it has its own scoring/model logic distinct from generic report AI calls | `opportunity_engine.py`, `scoring/` (impact, complexity, priority calculators), `models.py` | Turn extracted company data into ranked automation opportunities. See §7. |
| `pdf/` | Isolates ReportLab so report layout logic doesn't leak into services | `report_builder.py`, `templates/*.py`, `builders/*.py` (e.g., `cover_section.py`, `competitor_section.py`, `opportunity_section.py`) | Compose a PDF from already-generated report data. No data fetching. |
| `discord/` | Isolates outbound notification/delivery | `discord_client.py`, `message_formatter.py` | Send a finished report/summary to a Discord channel. |
| `models/` | Internal domain representation independent of API or DB shape | `company.py`, `competitor.py`, `report.py`, `opportunity.py` | Plain domain objects used across services; not tied to Pydantic or an ORM. |
| `schemas/` | The literal API contract, versionable and OpenAPI-visible | `company_schema.py`, `report_schema.py`, `competitor_schema.py`, `opportunity_schema.py`, `common.py` (envelope/error shapes) | Request/response DTOs with validation. Never used as internal domain models. |
| `utils/` | Avoid duplicated helper logic scattered across services | `url_utils.py`, `text_utils.py`, `hashing.py`, `retry.py` | Pure functions, no side effects, no framework imports. |
| `prompts/` | Prompts are content, not code — versioned and reviewed like copy | `company_summary.prompt.md`, `competitor_analysis.prompt.md`, `opportunity_scoring.prompt.md` | Prompt templates only. Loaded by `ai/` clients; never contain logic. |
| `clients/` | One thin wrapper per external API, isolating auth/retry/error-mapping | `base_client.py`, `http_client.py` | Shared HTTP client behavior (timeouts, retries, error translation) reused by `search/`, `ai/`, `crawler/`, `discord/`. |
| `middleware/` | Cross-cutting request lifecycle concerns | `error_handler.py`, `request_logging.py`, `rate_limiter.py`, `cors.py` | Runs on every request/response; never resource-specific. |

### Backend service interfaces (contracts, not implementations)

Defined in `backend/app/services/interfaces/`, each as a `Protocol`/ABC — signatures and docstrings
only:

- **`CompanyService`** — resolves a name/URL input into a canonical `Company` identity (domain,
  aliases) before downstream processing.
- **`SearchService`** — given a company identity, returns candidate web results (via Serper.dev).
- **`CrawlerService`** — given URLs, returns normalized page content (via Crawl4AI).
- **`AIService`** — given extracted content + a prompt template, returns structured AI output (via
  OpenRouter). Generic — used by report generation, competitor analysis, etc.
- **`CompetitorService`** — given a company profile, identifies and ranks competitors.
- **`OpportunityService`** — given a company profile, produces **AI Growth Opportunities™**
  (automation ideas, impact, complexity, priority). See §7.
- **`ReportService`** — the orchestrator; sequences Company → Search → Crawler → AI → Competitor →
  Opportunity → PDF and returns a finished report reference.
- **`DiscordService`** — delivers a finished report/summary to a configured Discord destination.

Each interface method signature is designed around **domain models** (`models/`) in, **domain
models** out — schemas only appear at the API boundary. This keeps services testable without FastAPI
or Pydantic in the loop.

---

## 4. Frontend — `frontend/src/`

React 18 + Vite + TypeScript + TailwindCSS + shadcn/ui + Framer Motion. Organized by **feature-aware
layering**: shared primitives vs. feature-specific composition.

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── ui/            # shadcn/ui primitives (button, card, dialog, input…)
│   │   ├── common/         # App-wide composed components (Navbar, Footer, Loader, ErrorBoundary)
│   │   ├── company/        # Company search/input feature components
│   │   ├── report/         # Report display feature components
│   │   ├── competitor/     # Competitor analysis feature components
│   │   └── opportunities/  # AI Growth Opportunities™ feature components
│   ├── pages/               # Route-level views (composition only)
│   ├── hooks/                # Reusable stateful logic (useCompanySearch, useReportStatus…)
│   ├── layouts/              # Page shells (AppLayout, AuthLayout if ever needed)
│   ├── services/             # Typed API client wrappers (one per backend resource)
│   ├── types/                # TypeScript types/interfaces mirroring backend schemas
│   ├── utils/                 # Pure helper functions (formatting, validation)
│   ├── styles/                 # Tailwind entry, design tokens, global CSS
│   ├── contexts/               # React Context providers (theme, report-session state)
│   ├── assets/                  # Images/icons/fonts bundled by Vite
│   └── config/                  # Frontend runtime config (API base URL, feature flags)
├── tests/
│   ├── unit/
│   └── integration/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.ts
└── .env.example
```

### Folder-by-folder responsibilities

| Folder | Why it exists | What belongs here | Responsibility |
|---|---|---|---|
| `components/ui/` | shadcn/ui's generated, unopinionated primitives — kept separate so codegen/updates don't collide with app code | `button.tsx`, `card.tsx`, `dialog.tsx`, etc. (generated via shadcn CLI in Phase 2) | Presentational only, no app state. |
| `components/common/` | Cross-feature building blocks used on every page | `Navbar`, `Footer`, `LoadingSpinner`, `ErrorBoundary`, `EmptyState` | Reusable, feature-agnostic UI. |
| `components/company/` | Encapsulates the company input/search feature | `CompanySearchForm`, `CompanySearchInput`, `RecentSearches` | UI for capturing name/URL input. |
| `components/report/` | Encapsulates report display | `ReportSummaryCard`, `ReportSectionList`, `ReportDownloadButton` | Renders a generated report. |
| `components/competitor/` | Encapsulates competitor analysis UI | `CompetitorTable`, `CompetitorCard` | Displays competitor findings. |
| `components/opportunities/` | Dedicated UI home for **AI Growth Opportunities™**, kept isolated because it's the differentiated/exclusive feature | `OpportunityList`, `OpportunityCard`, `PriorityBadge`, `ImpactComplexityMatrix` | Displays ranked automation opportunities. See §7. |
| `pages/` | Route targets, kept thin | `HomePage.tsx`, `ReportPage.tsx`, `CompetitorPage.tsx`, `OpportunitiesPage.tsx`, `NotFoundPage.tsx` | Compose layouts + feature components; no business logic. |
| `hooks/` | Reusable stateful/async logic decoupled from components | `useCompanySearch.ts`, `useReport.ts`, `useDebounce.ts`, `useApiRequest.ts` | Encapsulate data-fetching/state so components stay declarative. |
| `layouts/` | Consistent page chrome across routes | `AppLayout.tsx` | Wraps pages with Navbar/Footer/providers. |
| `services/` | The only place that talks to the backend HTTP API | `apiClient.ts` (base fetch/axios wrapper), `companyService.ts`, `reportService.ts`, `competitorService.ts`, `opportunityService.ts` | One typed function set per backend resource; components never call `fetch` directly. |
| `types/` | Single source of truth for shapes flowing through the UI | `company.ts`, `report.ts`, `competitor.ts`, `opportunity.ts`, `api.ts` (envelope/error types) | Mirrors backend `schemas/` so FE/BE contracts stay in sync. |
| `utils/` | Stateless helpers | `formatDate.ts`, `urlValidator.ts`, `scoreFormatter.ts` | Pure functions only. |
| `styles/` | Design tokens and global styling entry | `globals.css`, `tailwind.css` | Tailwind directives, CSS variables, theme tokens. |
| `contexts/` | Cross-component state that isn't worth a state library yet | `ThemeContext.tsx`, `ReportSessionContext.tsx` | Lightweight global state via React Context. |
| `assets/` | Static files bundled by the build | logos, icons, illustrations | No logic. |
| `config/` | Centralizes environment-driven frontend config | `env.ts` (reads `import.meta.env`), `constants.ts` | Single place components/services read config from — never `import.meta.env` scattered around. |

---

## 5. `shared/`

```
shared/
├── types/       # Contract definitions conceptually shared by FE/BE (kept in sync manually or via
│                  future OpenAPI codegen)
└── constants/    # Cross-cutting constants (e.g., opportunity priority levels, report status enum)
```

Why it exists: FastAPI (Pydantic) and React (TypeScript) can't literally share code across languages,
but they must agree on **shape**. `shared/` documents the canonical contract in language-neutral form
(JSON Schema / markdown) so `backend/app/schemas/` and `frontend/src/types/` are generated or
hand-kept in lockstep. In a later phase this can be upgraded to auto-generate `frontend/src/types/`
from the FastAPI OpenAPI spec.

---

## 6. `docs/`, `scripts/`, `assets/`, `config/`, `tests/`

| Folder | Purpose |
|---|---|
| `docs/` | `ARCHITECTURE.md` (this file), `API_DESIGN.md`, `ROADMAP.md`, `CODING_STANDARDS.md`, `diagrams/` (exported diagrams), `adr/` (Architecture Decision Records for future irreversible choices). |
| `scripts/` | Developer ergonomics: `setup.ps1`/`setup.sh` (bootstrap both apps), `dev.ps1` (run FE+BE concurrently), `lint.ps1`, `check-env.ps1`. No app logic. |
| `assets/` | Design assets not served by the app itself: `branding/` (logo source files), `screenshots/` (README imagery). Distinct from `frontend/src/assets/`, which *is* bundled into the app. |
| `config/environments/` | Environment templates (`\.env.development.example`, `\.env.production.example`) documenting what each deploy target (Vercel/Render) needs, separate from the per-app `.env.example` files which are the actual load targets. |
| `tests/` | Cross-cutting tests that exercise frontend+backend together: `e2e/` (Playwright, later), `integration/` (contract tests verifying FE types match BE schemas). Unit tests live next to their app (`frontend/tests`, `backend/tests`). |

---

## 7. AI Growth Opportunities™ — Architecture Reservation

This is the product's exclusive feature, so it gets **first-class module status** on both sides even
though implementation is deferred:

- **Backend**: `backend/app/ai/opportunities/` — houses the engine that will turn a company's
  extracted profile into ranked opportunities. Internally reserved for four concerns (each its own
  file, populated in Phase 2+):
  - `opportunity_engine.py` — orchestrates generation (calls `AIService` + scoring).
  - `scoring/impact_scorer.py` — estimated business impact.
  - `scoring/complexity_scorer.py` — implementation complexity.
  - `scoring/priority_calculator.py` — combines impact + complexity → priority score.
  - `models.py` — `Opportunity` domain model (`title`, `description`, `impact`, `complexity`,
    `priority_score`, `category`).
  - Exposed to the rest of the backend only through `services/interfaces/opportunity_service.py`.
- **Frontend**: `frontend/src/components/opportunities/` and `frontend/src/services/opportunityService.ts`
  + `frontend/src/types/opportunity.ts` — dedicated feature slice, not bolted onto the generic report
  view.
- **API**: reserved route module `backend/app/api/v1/routes/opportunity_routes.py` (empty router
  registered in `main.py`, no handlers yet) and schema module `backend/app/schemas/opportunity_schema.py`.

This ensures Phase 2 work on the flagship feature never requires restructuring — only filling in
already-scoped files.

---

## 8. Complete Data Flow (future runtime behavior)

```
                                   ┌───────────────────┐
                                   │        USER        │
                                   │ (Company Name/URL)  │
                                   └──────────┬──────────┘
                                              │
                                              ▼
                          ┌───────────────────────────────────────┐
                          │              FRONTEND (React)           │
                          │  components/company → services/*.ts     │
                          │  → typed fetch to backend API            │
                          └──────────────────┬────────────────────┘
                                              │  HTTPS / JSON
                                              ▼
                          ┌───────────────────────────────────────┐
                          │           BACKEND API (FastAPI)          │
                          │   api/v1/routes → services/interfaces     │
                          └──────────────────┬────────────────────┘
                                              │
                                              ▼
                          ┌───────────────────────────────────────┐
                          │            CompanyService                │
                          │   resolves name/URL → canonical Company   │
                          └──────────────────┬────────────────────┘
                                              │
                                              ▼
                          ┌───────────────────────────────────────┐
                          │             SearchService                 │
                          │        (Serper.dev via search/)            │
                          │   → candidate URLs / web presence           │
                          └──────────────────┬────────────────────┘
                                              │
                                              ▼
                          ┌───────────────────────────────────────┐
                          │             CrawlerService                 │
                          │        (Crawl4AI via crawler/)              │
                          │   → normalized page content                  │
                          └──────────────────┬────────────────────┘
                                              │
                                              ▼
                          ┌───────────────────────────────────────┐
                          │               AIService                     │
                          │       (OpenRouter via ai/, prompts/)          │
                          │  → structured company profile / summary       │
                          └──────────────────┬────────────────────┘
                                              │
                          ┌───────────────────┴────────────────────┐
                          ▼                                        ▼
          ┌───────────────────────────┐            ┌───────────────────────────────┐
          │      CompetitorService      │            │       OpportunityService        │
          │  → ranked competitor list    │            │  → AI Growth Opportunities™      │
          │                               │            │  (impact / complexity / priority) │
          └──────────────┬──────────────┘            └────────────────┬─────────────────┘
                          │                                              │
                          └──────────────────────┬───────────────────────┘
                                                  ▼
                                    ┌───────────────────────────┐
                                    │        ReportService         │
                                    │  aggregates all findings      │
                                    └──────────────┬───────────────┘
                                                  ▼
                                    ┌───────────────────────────┐
                                    │             PDF               │
                                    │   (ReportLab via pdf/)         │
                                    │  → downloadable report file     │
                                    └──────────────┬───────────────┘
                                                  ▼
                                    ┌───────────────────────────┐
                                    │          DiscordService        │
                                    │   (optional) → pushes summary   │
                                    └──────────────┬───────────────┘
                                                  ▼
                          ┌───────────────────────────────────────┐
                          │           BACKEND API RESPONSE            │
                          │   schemas/ → standardized JSON envelope     │
                          └──────────────────┬────────────────────┘
                                              │  HTTPS / JSON
                                              ▼
                          ┌───────────────────────────────────────┐
                          │              FRONTEND (React)             │
                          │  report/, competitor/, opportunities/       │
                          │        render final results                  │
                          └───────────────────────────────────────┘
```

Every arrow above is a **service interface boundary** — each stage depends only on the interface of
the stage before it, never its implementation. `ReportService` is the only component aware of the
full sequence.

---

## 9. Coding Conventions

### Python (backend)
- **Style**: PEP 8, enforced via `ruff` + `black`. Line length 100.
- **Typing**: full type hints everywhere; `mypy --strict` in CI (added in Phase 2 tooling).
- **Naming**: `snake_case` for functions/variables/modules, `PascalCase` for classes, `SCREAMING_SNAKE_CASE`
  for constants. Interfaces suffixed `Service` (e.g., `SearchService`), implementations prefixed
  `Default`/provider name (e.g., `DefaultSearchService`, `SerperSearchService`).
- **Files**: one class per file for services/clients; one router per resource for routes.
- **Imports**: absolute imports rooted at `app.` — no relative `..` imports across layers.
- **Async**: all I/O-bound service methods are `async def`; clients use `httpx.AsyncClient`.

### TypeScript (frontend)
- **Style**: ESLint (airbnb-ish + React hooks plugin) + Prettier.
- **Naming**: `PascalCase` for components/types/interfaces, `camelCase` for functions/variables/hooks
  (`useX` prefix mandatory for hooks), `kebab-case` for non-component file names where relevant.
- **Components**: function components only, colocated with a `.test.tsx` in Phase 2.
- **Types**: prefer `interface` for object shapes that mirror API contracts, `type` for unions/utility
  types.
- **Imports**: absolute imports via `@/` alias (configured in `tsconfig.json` / `vite.config.ts`), no
  deep relative `../../../` chains.

### General
- No commented-out code committed.
- No `console.log` / `print` left in committed code — use the logging strategy (§12).
- Every public function/class has a docstring describing *why*, not *what* (name should cover *what*).

---

## 10. API Response Format

All responses use a consistent envelope so the frontend has one parsing path. **Implemented** in
`backend/app/schemas/common.py` (`SuccessResponse[T]`, `BaseResponse`, `ResponseMeta`) — this is no
longer just a design sketch.

**Success:**
```json
{
  "success": true,
  "data": { "...resource-specific payload..." },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-08-02T10:00:00+00:00"
  }
}
```

**Paginated success:**
```json
{
  "success": true,
  "data": [ "...items..." ],
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-08-02T10:00:00+00:00",
    "page": 1,
    "page_size": 20,
    "total": 57
  }
}
```

Built via `app.utils.response_helper.build_success_response`; mirrored in
`frontend/src/types/api.ts` (camelCase there, since that's the TS convention — the two sides agree on
structure, not literal key casing).

---

## 11. Error Response Format

**Implemented** in `backend/app/schemas/common.py` (`ErrorResponse`, `ApiError`) and produced
exclusively by `backend/app/middleware/error_handler.py`.

```json
{
  "success": false,
  "error": {
    "code": "COMPANY_NOT_FOUND",
    "message": "No company could be resolved from the given input.",
    "details": []
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-08-02T10:00:00+00:00"
  }
}
```

- `code` is a stable, machine-readable string (`SCREAMING_SNAKE_CASE`) defined in
  `backend/app/core/exceptions.py` (the `AppError` taxonomy) or derived from the HTTP status for
  framework-raised `HTTPException`s; the frontend can switch on it without parsing `message`.
- `message` is human-readable, safe to display.
- `details` is a list of short strings (e.g., one per validation failure) and never leaks stack
  traces or internal paths.
- HTTP status is set appropriately (400/404/422/429/500/501) — the envelope shape stays constant
  across all of them.
- Four handlers, registered together by `register_exception_handlers(app)`, are the **only** place
  this shape is produced: validation errors (422), `HTTPException`s (whatever status was raised —
  this is how the current `501 Not Implemented` stub routes respond), domain `AppError`s (status per
  exception class), and anything unhandled (500, logged with full traceback server-side, generic
  message client-side).

---

## 12. Logging Strategy

- **Backend**: structured JSON logging (stdlib `logging` only, no third-party logging library) —
  configured once in `core/logging.py` (`configure_logging`, called from `app.main`'s lifespan).
  Every log line includes `request_id`, `service`, `level`, `message`, `timestamp`, emitted to both
  the console and a rotating file (`backend/logs/app.log`, 5MB × 5 backups). `request_id` is
  generated/propagated by `middleware/request_id.py` via a `contextvars.ContextVar` and echoed in
  the `X-Request-ID` response header and every API response's `meta.request_id` for correlation.
  Any other module obtains a logger via `app.utils.logger.get_logger(__name__)`.
  - `DEBUG`: local dev only (raw payloads from external APIs, prompt contents).
  - `INFO`: request lifecycle, service-level milestones (e.g., "crawl completed: 12 pages").
  - `WARNING`: recoverable issues (e.g., a competitor lookup returned zero results).
  - `ERROR`: unhandled exceptions, third-party API failures after retries exhausted.
  - Never log API keys, full prompt payloads in production, or raw user PII beyond what's needed.
- **Frontend**: a thin `logger.ts` utility in `utils/` wraps `console.*`, disabled/minimized in
  production builds; real error tracking (e.g., Sentry) is a Phase 2+ decision, left as an ADR.

---

## 13. Configuration Strategy

- **Backend**: `pydantic-settings` `Settings` class in `core/config.py` loads from environment
  variables (`.env` locally, real env vars on Render). One `Settings` instance is constructed once
  and injected via DI (`core/container.py`) — no module reaches into `os.environ` directly outside
  `core/config.py`.
- **Frontend**: Vite's `import.meta.env.VITE_*` variables are read **only** inside `src/config/env.ts`,
  which exports a typed `config` object. Components/services import from `config/`, never read
  `import.meta.env` directly.
- **Per-environment templates** live in `config/environments/` (documentation/reference); the actual
  files each app loads are `frontend/.env.example` and `backend/.env.example`.
- No secrets are ever committed — only `.env.example` files with placeholder values.

---

## 14. Testing Strategy (scaffold only)

- `backend/tests/unit/` — tests against service interfaces using fakes/mocks for clients.
- `backend/tests/integration/` — tests that hit FastAPI's `TestClient` against a real DI graph with
  faked external clients.
- `frontend/tests/unit/` — component/hook tests (Vitest + Testing Library).
- `frontend/tests/integration/` — page-level flows with mocked `services/`.
- `tests/e2e/` — full-stack Playwright flows (Phase 3+, after real endpoints exist).
- `tests/integration/` — contract tests asserting `frontend/src/types/*` structurally match
  `backend/app/schemas/*` (via generated JSON schema comparison).

---

## 15. Deployment Topology

```
Vercel (frontend/)  ──HTTPS──▶  Render (backend/)  ──HTTPS──▶  Serper.dev / OpenRouter / Discord
                                        │
                                        ▼
                                  Crawl4AI (in-process or Render worker)
```

- Frontend build: `frontend/` deployed as a static Vite build on Vercel, `VITE_API_BASE_URL` points
  to the Render backend URL.
- Backend: `backend/` deployed as a FastAPI service on Render (Uvicorn/Gunicorn), CORS restricted to
  the Vercel domain via `middleware/cors.py`.
- No shared filesystem between FE/BE — all communication is via the versioned HTTP API (`/api/v1`).
