# Shared Types

Language-neutral documentation of contract shapes that both `backend/app/schemas/` (Pydantic) and
`frontend/src/types/` (TypeScript) must agree on. FastAPI/Pydantic and React/TypeScript can't share
code directly, so this folder is the canonical reference until an OpenAPI-codegen pipeline (Phase 8+
candidate, see [docs/adr/](../../docs/adr/)) can generate `frontend/src/types/` automatically from the
backend's OpenAPI spec.

Until then: any field added to a backend schema must be added to the matching frontend type in the
same change — see the review checklist in [docs/CODING_STANDARDS.md](../../docs/CODING_STANDARDS.md).
