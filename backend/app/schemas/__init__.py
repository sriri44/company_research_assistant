"""Pydantic request/response DTOs — the literal, versioned API contract.

Distinct from `app.models` (internal domain objects): schemas exist only at
the HTTP boundary and are never passed between services directly. One
module per resource (`report_schema.py`, `system_schema.py`; more land as
each resource's real endpoints do — `company_schema.py`,
`competitor_schema.py`, `opportunity_schema.py`), plus `common.py` for the
shared response/error envelope.
"""
