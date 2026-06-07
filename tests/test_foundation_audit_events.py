import json
import os

import pytest
from sqlalchemy import create_engine, text


@pytest.fixture(autouse=True)
def set_database_environment(monkeypatch, tmp_path):
    db_path = tmp_path / "audit_events.db"
    database_url = f"sqlite+aiosqlite:///{db_path}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    yield


@pytest.fixture
def create_audit_table():
    database_url = os.environ["DATABASE_URL"]
    engine = create_engine(database_url.replace("+aiosqlite", ""), echo=False, future=True)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    aggregate_type TEXT,
                    aggregate_id TEXT,
                    actor_id TEXT,
                    correlation_id TEXT,
                    payload JSON NOT NULL,
                    created_at DATETIME NOT NULL
                )
                """
            )
        )
    yield database_url
    engine.dispose()


def test_audit_event_inserts_into_audit_events_table(create_audit_table):
    from foundation.eligibility.audit import audit_event

    audit_event(
        "transfer_requested",
        {"request": {"student_id": "s1", "target_school_id": "school-1"}},
        aggregate_type="transfer",
        aggregate_id="s1",
        actor_id="SYSTEM",
        correlation_id="corr-123",
    )

    engine = create_engine(create_audit_table.replace("+aiosqlite", ""), echo=False, future=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT event_type, aggregate_type, aggregate_id, actor_id, correlation_id, payload FROM audit_events"))
        row = result.first()

    assert row is not None
    assert row[0] == "transfer_requested"
    assert row[1] == "transfer"
    assert row[2] == "s1"
    assert row[3] == "SYSTEM"
    assert row[4] == "corr-123"

    payload = json.loads(row[5]) if isinstance(row[5], str) else row[5]
    assert payload["request"]["student_id"] == "s1"
