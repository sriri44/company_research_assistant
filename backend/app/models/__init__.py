"""Internal domain models.

These are plain, framework-agnostic representations of core business concepts
(Company, Competitor, Opportunity, Report). They are distinct from
`app.schemas`, which defines the HTTP-facing (Pydantic) request/response
contracts. Services speak in domain models; the API layer translates at the
boundary.
"""
