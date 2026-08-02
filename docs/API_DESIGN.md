# API Design Overview

Status: **the real research pipeline is live.** `POST /api/v1/research` runs the full
resolve → search → crawl → extract → AI analysis → competitors → AI Growth Opportunities™ pipeline
end to end. Health/version endpoints remain live and functional. `company`, `report`, and
`opportunities` remain `501` stubs — their functionality is currently reached only through the
combined `/research` pipeline (see `docs/ARCHITECTURE.md`'s "one AI call" note in
`research_report_service.py`), not through their own dedicated endpoints yet.

Versioned endpoints are mounted under `/api/v1`. Root-level health/liveness probes are **unversioned**
(no prefix), since infra platforms (Render, load balancers, uptime monitors) expect stable paths.
Base URL in production is the Render backend domain; locally, `http://localhost:8000`.

---

## 1. Resource Map

| Router file | Base path | Status | Purpose |
|---|---|---|---|
| `health_routes.py` | `/`, `/health`, `/ready`, `/version` | **Live** | Root-level liveness/readiness/version probes. Never call an external service or a service implementation. |
| `research_routes.py` | `POST /api/v1/research`, `GET /api/v1/research/{id}` | **Live** | The full AI research pipeline: resolve → search → crawl → extract → one AI call → competitors + AI Growth Opportunities™. |
| `company_routes.py` | `/api/v1/company` | 501 stub | Dedicated company-resolution endpoint (resolution already works via `/research`, internally). |
| `report_routes.py` | `/api/v1/report` | 501 stub | Dedicated async report job endpoints (current `/research` is synchronous). |
| `opportunity_routes.py` | `/api/v1/opportunities` | 501 stub | Dedicated opportunities-only endpoint (`AIOpportunityService` is implemented and real, just not routed standalone yet). |
| `system_routes.py` | `/api/v1/system` | 501 stub | Reserved for versioned, API-consumer-facing diagnostics (distinct from the unversioned `/health`). |

`competitor_routes.py` and `discord_routes.py` are reserved for later phases. Every stub handler
already resolves its real service via FastAPI `Depends()` — the DI graph is proven end to end — it
just never calls a method on it.

### `POST /api/v1/research` — the real pipeline

Request:
```json
{ "query": "stripe.com", "model": "openai/gpt-4o-mini" }
```
`query` accepts a company name *or* a website URL/domain (URLs skip the search-resolution step
entirely); `model` is optional and falls back to `OPENROUTER_DEFAULT_MODEL`.

Response (`SuccessResponse<ResearchResultSchema>`):
```json
{
  "success": true,
  "data": {
    "report_id": "uuid",
    "status": "complete",
    "company_name": "Stripe",
    "website": "stripe.com",
    "phone": null,
    "address": null,
    "summary": "...",
    "industry": "Financial Infrastructure & Payments",
    "products": ["..."],
    "services": ["..."],
    "pain_points": ["..."],
    "competitors": [{ "name": "Adyen", "website": "adyen.com", "reason": "...", "market_position": "..." }],
    "growth_opportunities": [
      { "title": "...", "description": "...", "business_impact": "high",
        "implementation_complexity": "medium", "priority_score": 88, "estimated_roi": "..." }
    ],
    "sources": ["https://stripe.com/", "https://stripe.com/pricing"],
    "confidence": 0.8
  },
  "meta": { "request_id": "uuid", "timestamp": "2026-08-02T10:00:00+00:00" }
}
```
`status` can be `"complete"` or `"failed"` — a crawl/search failure degrades gracefully (the AI still
runs on whatever was gathered); only a total AI failure returns `status: "failed"` with an
explanatory `summary`, still as HTTP 200 (there is a result, just an incomplete one). Company
resolution failure (no website found for a name) is the one case that returns an HTTP error
(`404 COMPANY_NOT_FOUND`), since nothing else can proceed without it.

### `GET /api/v1/research/{report_id}`
Fetches a previously completed run from the in-memory report cache (no database yet — reports don't
survive a process restart). Returns `404 REPORT_NOT_FOUND` for an unknown id.

---

## 2. Implemented Endpoints (health/version — live, no external calls)

### `GET /health`
```json
{
  "success": true,
  "data": { "status": "ok", "timestamp": "2026-08-02T10:00:00+00:00" },
  "meta": { "request_id": "uuid", "timestamp": "2026-08-02T10:00:00+00:00" }
}
```

### `GET /version`
```json
{
  "success": true,
  "data": { "app_name": "AI Company Research Assistant API", "app_version": "0.1.0", "app_env": "development" },
  "meta": { "request_id": "uuid", "timestamp": "2026-08-02T10:00:00+00:00" }
}
```

## 3. Conceptual Request/Response Shapes for the remaining stub resources

These are **illustrative only** — they define the contract style each 501 stub will fill in, not
final field lists. Note the underlying service logic they'd call already exists and is real
(`DefaultCompanyService`, `ResearchReportService`, `AIOpportunityService`) — only the dedicated
standalone routes are still stubs.

### `POST /api/v1/company/resolve`
Request: `{ "input": "acme.com" }` → `SuccessResponse<Company>`.

### `POST /api/v1/report`
Request: `{ "companyId": "uuid" }` → `SuccessResponse<JobStatus>` (see
`backend/app/schemas/report_schema.py`). Long-running orchestration implies this becomes async (poll
`GET /api/v1/report/{id}`, or later a streaming status channel — left as an ADR for Phase 6).

### `GET /api/v1/opportunities/{companyId}`
→ `SuccessResponse<Opportunity[]>` — each item: `{ title, description, category, impact, complexity,
priorityScore }`.

All shapes above are defined as Pydantic schemas in `backend/app/schemas/` and mirrored as TS
interfaces in `frontend/src/types/`. See [ARCHITECTURE.md §10–11](ARCHITECTURE.md#10-api-response-format)
for the response/error envelope every one of these wraps into.

---

## 4. Versioning Strategy

- URL-path versioning (`/api/v1`) for all resource endpoints — a breaking contract change ships as
  `/api/v2` alongside `/v1` until the frontend migrates, then `/v1` is deprecated (never silently
  mutated).
- Root health/liveness probes (`/`, `/health`, `/ready`, `/version`) are intentionally **not**
  versioned — infrastructure tooling depends on their path never moving.
- Schema evolution within a version must be additive-only (new optional fields), enforced by review,
  not tooling, in this phase.

## 5. Auth (deferred)

No authentication yet (public research tool). `middleware/` has no auth middleware by design this
phase — a rate-limit/API-key gate is a pre-launch ADR, not part of this infrastructure pass.

## 6. Rate Limiting & Cost Control

Because Search, Crawl, and AI calls will cost money per request once implemented, a
`middleware/rate_limiter.py` is reserved to throttle per-IP or per-session request rates before those
calls ship — called out explicitly so that phase doesn't skip it.
