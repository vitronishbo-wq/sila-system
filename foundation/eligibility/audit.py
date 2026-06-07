import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import JSON, Column, DateTime, Integer, MetaData, String, Table, insert
from sqlalchemy.ext.asyncio import AsyncSession

LOG_PATH = Path("reports") / "eligibility_audit.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("eligibility_audit")
logger.setLevel(logging.INFO)
# Do NOT attach a file handler by default. Primary audit destination is the
# `audit_events` DB table. File fallback is handled explicitly by
# `_write_fallback_log()` when DB operations fail.

metadata = MetaData()
audit_events_table = Table(
    "audit_events",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_type", String(100), nullable=False),
    Column("aggregate_type", String(100), nullable=True),
    Column("aggregate_id", String(100), nullable=True),
    Column("actor_id", String(100), nullable=True),
    Column("correlation_id", String(100), nullable=True),
    Column("payload", JSON, nullable=False),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
)


def _run_coroutine_in_thread(coro_factory, *args, **kwargs):
    from concurrent.futures import ThreadPoolExecutor

    def runner():
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro_factory(*args, **kwargs))
        finally:
            loop.close()

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(runner)
        return future.result()


def _run_sync(coro_factory, *args, **kwargs):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro_factory(*args, **kwargs))
    return _run_coroutine_in_thread(coro_factory, *args, **kwargs)


def _load_db_transaction():
    try:
        from apps.backend.app.core.db import transaction

        return transaction
    except Exception as exc:
        raise RuntimeError("Database infrastructure is unavailable") from exc


def _resolve_audit_fields(
    event_type: str,
    payload: dict,
    aggregate_type: str | None = None,
    aggregate_id: str | None = None,
    actor_id: str | None = None,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    aggregate_type = aggregate_type or payload.get("aggregate_type") or payload.get("entity_type")
    aggregate_id = aggregate_id or payload.get("aggregate_id") or payload.get("request", {}).get("student_id")
    actor_id = actor_id or payload.get("actor_id")
    correlation_id = correlation_id or payload.get("correlation_id")
    return {
        "event_type": event_type,
        "aggregate_type": aggregate_type,
        "aggregate_id": aggregate_id,
        "actor_id": actor_id,
        "correlation_id": correlation_id,
        "payload": payload or {},
        "created_at": datetime.utcnow(),
    }


def _write_fallback_log(event_type: str, payload: dict) -> None:
    # Append a JSON line to the fallback log file. Create parent dir if needed.
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {"event": event_type, "payload": payload, "fallback": True}
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # Swallow any filesystem errors; logging must not raise.
        logger.exception("Failed to write fallback audit log")


async def _insert_audit_event(
    event_type: str,
    payload: dict,
    aggregate_type: str | None = None,
    aggregate_id: str | None = None,
    actor_id: str | None = None,
    correlation_id: str | None = None,
    session: AsyncSession | None = None,
) -> None:
    values = _resolve_audit_fields(
        event_type,
        payload,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        actor_id=actor_id,
        correlation_id=correlation_id,
    )
    stmt = insert(audit_events_table).values(**values)
    if session is not None:
        await session.execute(stmt)
        return

    try:
        transaction = _load_db_transaction()
        async with transaction() as session:
            await session.execute(stmt)
        return
    except Exception:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise
        from sqlalchemy.ext.asyncio import create_async_engine

        engine = create_async_engine(database_url, future=True)
        try:
            async with engine.begin() as conn:
                await conn.execute(stmt)
        finally:
            await engine.dispose()


async def audit_event_async(
    event_type: str,
    payload: dict,
    aggregate_type: str | None = None,
    aggregate_id: str | None = None,
    actor_id: str | None = None,
    correlation_id: str | None = None,
    session: AsyncSession | None = None,
) -> None:
    """Write an audit event to the audit_events table inside an async session."""
    await _insert_audit_event(
        event_type,
        payload,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        actor_id=actor_id,
        correlation_id=correlation_id,
        session=session,
    )


def audit_event(
    event_type: str,
    payload: dict,
    aggregate_type: str | None = None,
    aggregate_id: str | None = None,
    actor_id: str | None = None,
    correlation_id: str | None = None,
) -> None:
    """Write an audit event to the audit_events table."""
    try:
        _run_sync(
            _insert_audit_event,
            event_type,
            payload,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
    except Exception as exc:
        logger.warning(
            "Audit DB insert failed, falling back to local audit log: %s",
            str(exc),
        )
        _write_fallback_log(event_type, payload)
