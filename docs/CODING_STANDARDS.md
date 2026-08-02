# Coding Standards — Quick Reference

Full rationale lives in [ARCHITECTURE.md §9](ARCHITECTURE.md#9-coding-conventions). This file is the
skimmable checklist used in code review.

## Naming cheat sheet

| Element | Convention | Example |
|---|---|---|
| Python module/function/variable | `snake_case` | `search_service.py`, `resolve_company()` |
| Python class | `PascalCase` | `SearchService`, `DefaultAIService` |
| Python constant | `SCREAMING_SNAKE_CASE` | `MAX_CRAWL_DEPTH` |
| Service interface | `<Noun>Service` | `OpportunityService` |
| Service implementation | `<Provider/Default><Noun>Service` | `SerperSearchService`, `DefaultReportService` |
| Pydantic schema | `<Noun>Schema` / `<Noun>Request` / `<Noun>Response` | `CompanySchema`, `ReportRequest` |
| Domain model | `<Noun>` (no suffix) | `Company`, `Opportunity` |
| TS component | `PascalCase.tsx` | `CompetitorTable.tsx` |
| TS hook | `useCamelCase.ts` | `useReportStatus.ts` |
| TS service function file | `camelCaseService.ts` | `opportunityService.ts` |
| TS type/interface | `PascalCase` | `interface Opportunity { ... }` |
| Env var | `SCREAMING_SNAKE_CASE`, prefixed `VITE_` for frontend-exposed | `OPENROUTER_API_KEY`, `VITE_API_BASE_URL` |
| API error code | `SCREAMING_SNAKE_CASE` | `COMPANY_NOT_FOUND` |
| Route path | `kebab-case`, plural nouns | `/api/v1/competitor-analysis` (if multi-word ever needed) |

## Branching & commits (recommended, adopt when git is initialized)
- Branches: `phase-<n>/<short-description>` (e.g., `phase-2/company-resolution`).
- Commits: conventional style — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- No direct commits to `main` once collaborators > 1 — PR review required.

## Review checklist
- [ ] No business logic in `api/routes/` or `pages/`.
- [ ] New service has an interface in `services/interfaces/` before an implementation.
- [ ] No secrets committed; `.env.example` updated if a new var was introduced.
- [ ] New API field added to both `backend/app/schemas/` and `frontend/src/types/`.
- [ ] Errors raised via `core/exceptions.py` taxonomy, not bare `HTTPException` with inline strings.
- [ ] No `console.log`/`print` left in.
