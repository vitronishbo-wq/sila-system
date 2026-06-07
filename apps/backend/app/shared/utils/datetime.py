from __future__ import annotations

from datetime import UTC, datetime


def utcnow() -> datetime:
    return datetime.now(UTC)


def to_iso8601(dt: datetime) -> str:
    return dt.astimezone(UTC).isoformat()
