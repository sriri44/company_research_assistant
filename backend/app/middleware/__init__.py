"""Cross-cutting request/response middleware: `request_id.py`, `timing.py`,
`cors.py`, `trusted_hosts.py`, `gzip.py`, `security_headers.py`,
`error_logging.py`, and `error_handler.py` (global exception handlers).
Registered once in `app.main.create_app`. Never resource-specific.
`rate_limiter.py` is reserved for a later phase, once paid upstream calls
(Serper/OpenRouter) exist to protect.
"""
