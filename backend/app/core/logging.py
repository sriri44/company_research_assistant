"""Structured logging setup.

Configures the stdlib `logging` root logger (no third-party logging
library) to emit structured JSON lines — console + a rotating log file —
with `timestamp`, `level`, `service`, `message`, and `request_id` fields
(docs/ARCHITECTURE.md §12). `request_id` is populated from `request_id_var`,
a context variable set per-request by `app.middleware.request_id`, so every
log line emitted while handling a request is automatically correlated.

Call `configure_logging` exactly once, at application startup (see
`app.main`'s lifespan). Everywhere else, obtain a logger via
`app.utils.logger.get_logger` — never call `logging.basicConfig` again.
"""

from __future__ import annotations

import json
import logging
import logging.handlers
import sys
from contextvars import ContextVar
from pathlib import Path

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

_LOG_DIR = Path("logs")
_LOG_FILE = _LOG_DIR / "app.log"
_MAX_BYTES = 5 * 1024 * 1024
_BACKUP_COUNT = 5


class RequestIdFilter(logging.Filter):
    """Attaches the current request id (if any) to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


class JsonFormatter(logging.Formatter):
    """Renders each log record as a single structured JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "service": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging(log_level: str = "INFO") -> None:
    """Initialize application-wide logging: a console handler and a
    rotating file handler, both emitting structured JSON at `log_level`.
    Idempotent — safe to call once at startup."""
    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers.clear()

    formatter = JsonFormatter()
    request_filter = RequestIdFilter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(request_filter)
    root.addHandler(console_handler)

    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=_LOG_FILE,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(request_filter)
    root.addHandler(file_handler)
