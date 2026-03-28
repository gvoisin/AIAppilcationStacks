import json
import logging
import os
from typing import Any

LOGGER_NAME = "server.external"
REDACTED = "***REDACTED***"
SENSITIVE_KEYS = {
    "authorization",
    "api-key",
    "api_key",
    "x-api-key",
    "proxy-authorization",
    "cookie",
    "set-cookie",
    "password",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "db_password",
    "wallet_password",
    "openai_inno_dev1",
}
MAX_PREVIEW_LEN = 4000
MAX_ITEMS = 20


def resolve_log_level() -> int:
    raw_level = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, raw_level, logging.INFO)


def setup_logging() -> None:
    logging.basicConfig(
        level=resolve_log_level(),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def get_external_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def is_debug_enabled(logger: logging.Logger | None = None) -> bool:
    active_logger = logger or get_external_logger()
    return active_logger.isEnabledFor(logging.DEBUG)


def _is_sensitive_key(key: str) -> bool:
    lowered = key.lower()
    return lowered in SENSITIVE_KEYS or any(token in lowered for token in ("secret", "token", "password", "authorization", "cookie", "api_key", "api-key"))


def sanitize_for_logging(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            sanitized[key] = REDACTED if _is_sensitive_key(str(key)) else sanitize_for_logging(item)
        return sanitized
    if isinstance(value, (list, tuple, set)):
        items = list(value)
        sanitized_items = [sanitize_for_logging(item) for item in items[:MAX_ITEMS]]
        if len(items) > MAX_ITEMS:
            sanitized_items.append(f"...({len(items) - MAX_ITEMS} more items)")
        return sanitized_items
    if isinstance(value, bytes):
        return f"<bytes {len(value)} bytes>"
    if hasattr(value, "read") and callable(value.read):
        return f"<{type(value).__name__}>"
    if isinstance(value, str):
        if len(value) > MAX_PREVIEW_LEN:
            return f"{value[:MAX_PREVIEW_LEN]}...<truncated {len(value) - MAX_PREVIEW_LEN} chars>"
        return value
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    if hasattr(value, "model_dump") and callable(value.model_dump):
        try:
            return sanitize_for_logging(value.model_dump())
        except Exception:
            return repr(value)
    if hasattr(value, "dict") and callable(value.dict):
        try:
            return sanitize_for_logging(value.dict())
        except Exception:
            return repr(value)
    if hasattr(value, "__dict__"):
        try:
            return sanitize_for_logging(vars(value))
        except Exception:
            return repr(value)
    return repr(value)


def serialize_for_logging(value: Any) -> str:
    sanitized = sanitize_for_logging(value)
    try:
        return json.dumps(sanitized, ensure_ascii=False, default=str)
    except Exception:
        return repr(sanitized)


def summarize_rows(columns: list[str] | None, rows: list[Any], limit: int = 5) -> dict[str, Any]:
    preview_rows = []
    for row in rows[:limit]:
        if columns and isinstance(row, (list, tuple)):
            preview_rows.append({col: sanitize_for_logging(val) for col, val in zip(columns, row)})
        else:
            preview_rows.append(sanitize_for_logging(row))
    summary: dict[str, Any] = {
        "row_count": len(rows),
        "preview": preview_rows,
    }
    if columns:
        summary["columns"] = columns
    if len(rows) > limit:
        summary["truncated"] = len(rows) - limit
    return summary


def log_external_request(logger: logging.Logger, target: str, url: str | None, request_payload: Any, extra: dict[str, Any] | None = None) -> None:
    if not is_debug_enabled(logger):
        return
    payload = {
        "target": target,
        "url": url,
        "request": sanitize_for_logging(request_payload),
    }
    if extra:
        payload["extra"] = sanitize_for_logging(extra)
    logger.debug("External request: %s", serialize_for_logging(payload))


def log_external_response(logger: logging.Logger, target: str, url: str | None, response_payload: Any, extra: dict[str, Any] | None = None) -> None:
    if not is_debug_enabled(logger):
        return
    payload = {
        "target": target,
        "url": url,
        "response": sanitize_for_logging(response_payload),
    }
    if extra:
        payload["extra"] = sanitize_for_logging(extra)
    logger.debug("External response: %s", serialize_for_logging(payload))


def log_external_error(logger: logging.Logger, target: str, url: str | None, request_payload: Any, error: Exception | str, extra: dict[str, Any] | None = None) -> None:
    payload = {
        "target": target,
        "url": url,
        "request": sanitize_for_logging(request_payload),
        "error": str(error),
    }
    if extra:
        payload["extra"] = sanitize_for_logging(extra)
    logger.exception("External error: %s", serialize_for_logging(payload))
