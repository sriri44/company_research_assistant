"""Resource route modules (one file per resource):

- `health_routes.py`   — unversioned root probes (/, /health, /ready,
  /version). Fully implemented; makes no external calls.
- `company_routes.py`, `research_routes.py`, `report_routes.py`,
  `opportunity_routes.py`, `system_routes.py` — mounted under `/api/v1`.
  Each resolves its service via `Depends()` but currently returns
  HTTP 501 — see docs/ROADMAP.md for when each becomes real.

`competitor_routes.py` and `discord_routes.py` are reserved for later
phases (competitor analysis is folded into `research_routes.py` for now;
Discord delivery has no route yet). Every module only parses requests and
delegates to a service; no business logic here.
"""
