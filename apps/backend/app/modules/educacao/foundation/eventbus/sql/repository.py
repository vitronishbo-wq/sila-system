from __future__ import annotations

import datetime
import logging
import os
from typing import Any

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from .models import Base, OutboxEvent

logger = logging.getLogger(__name__)


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/foundation_outbox.db")


def get_engine(url: str | None = None):
    return create_engine(url or DATABASE_URL, future=True)


def ensure_schema(engine=None):
    eng = engine or get_engine()
    Base.metadata.create_all(eng)


def get_session(engine=None):
    eng = engine or get_engine()
    return sessionmaker(bind=eng, future=True)


class OutboxRepository:
    def __init__(self, engine=None):
        self.engine = engine or get_engine()
        self.Session = sessionmaker(bind=self.engine, future=True)

    def enqueue(self, topic: str, payload: dict[str, Any], tenant_id: str | None = None) -> int:
        with self.Session() as sess:
            ev = OutboxEvent(topic=topic, payload=payload, tenant_id=tenant_id)
            sess.add(ev)
            sess.commit()
            sess.refresh(ev)
            return ev.id

    def claim_events(self, worker_id: str, limit: int = 50) -> list[OutboxEvent]:
        """Atomically claim a batch of events by setting locked_by/locked_at.

        Uses an UPDATE ... WHERE dispatched=false AND locked_by IS NULL
        pattern and then returns the claimed rows. Works best on Postgres.
        For sqlite this falls back to selecting unlocked rows and updating them.
        """
        with self.engine.begin() as conn:
            dialect = conn.dialect.name
            now = datetime.datetime.utcnow()
            if dialect in ("postgresql",):
                # Postgres supports UPDATE ... RETURNING
                stmt = (
                    update(OutboxEvent)
                    .where(OutboxEvent.dispatched == False, OutboxEvent.locked_by == None)
                    .values(locked_by=worker_id, locked_at=now)
                    .returning(OutboxEvent)
                    .limit(limit)
                )
                res = conn.execute(stmt)
                rows = res.fetchall()
                events = [r[0] if isinstance(r, tuple) else r for r in rows]
                return events

            # Fallback: use a Session to select objects, then atomically update their locked fields
            Session = sessionmaker(bind=conn.engine, future=True)
            with Session() as sess:
                rows = sess.query(OutboxEvent).filter(OutboxEvent.dispatched == False, OutboxEvent.locked_by == None).limit(limit).with_for_update(skip_locked=True).all()
                ids = [r.id for r in rows]
                if not ids:
                    return []
                # claim by updating locked fields
                sess.execute(
                    update(OutboxEvent).where(OutboxEvent.id.in_(ids)).values(locked_by=worker_id, locked_at=now)
                )
                sess.commit()
                claimed = sess.query(OutboxEvent).filter(OutboxEvent.id.in_(ids)).all()
                return claimed

    def mark_dispatched(self, ids: list[int]) -> None:
        if not ids:
            return
        with self.engine.begin() as conn:
            stmt = (
                update(OutboxEvent)
                .where(OutboxEvent.id.in_(ids))
                .values(dispatched=True, dispatched_at=datetime.datetime.utcnow())
            )
            conn.execute(stmt)

    def release_locks(self, ids: list[int]) -> None:
        if not ids:
            return
        with self.engine.begin() as conn:
            stmt = (
                update(OutboxEvent)
                .where(OutboxEvent.id.in_(ids))
                .values(locked_by=None, locked_at=None)
            )
            conn.execute(stmt)

    def increment_attempts(self, id: int) -> None:
        with self.engine.begin() as conn:
            stmt = (
                update(OutboxEvent)
                .where(OutboxEvent.id == id)
                .values(attempts=OutboxEvent.attempts + 1)
            )
            conn.execute(stmt)
