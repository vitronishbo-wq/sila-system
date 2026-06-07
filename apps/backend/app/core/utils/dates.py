"""Date/time conversion helpers."""

from typing import Any


def safe_isoformat(value: Any) -> str | None:
    """Converte date/datetime em ISO8601; retorna None se inválido."""
    if value is None:
        return None
    try:
        return value.isoformat()
    except (AttributeError, TypeError):
        return None
