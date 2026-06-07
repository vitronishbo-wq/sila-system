import os
import time

os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379/0")

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from foundation.automation.automator import AutomationEngine
from foundation.automation.message_bus import LocalAutomationBus
from foundation.orchestration.orchestrator import Orchestrator


def read_audit_events():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        engine = create_async_engine(database_url, echo=False, future=True)
        try:
            async def query():
                async with engine.connect() as conn:
                    result = await conn.execute(text("SELECT event_type FROM audit_events ORDER BY created_at DESC LIMIT 1"))
                    row = result.first()
                    return row[0] if row else ""

            return __import__("asyncio").run(query())
        except Exception:
            return ""
        finally:
            __import__("asyncio").run(engine.dispose())

    path = os.path.join("reports", "eligibility_audit.log")
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_async_transfer_scheduled_and_executed():
    orch = Orchestrator()
    auto = AutomationEngine(orchestrator=orch)

    req = {
        "student_id": "s1",
        "target_school": "school-1",
        "target_class": "9",
        "academic_year": "2026",
        "date_of_birth": "2012-05-01",
        "debts": [],
        "sanctions": [],
        "institution_capacity": {"available": 1},
    }

    resp = auto.request_transfer(req, async_execute=True)
    assert resp["status"] == "scheduled"

    # wait for worker to process
    time.sleep(1.0)

    log = read_audit_events()
    assert "transfer_completed" in log or "transfer_executed" in log

    auto.stop()


def test_async_transfer_scheduled_and_executed_with_local_bus():
    bus = LocalAutomationBus()
    auto = AutomationEngine(bus=bus)

    req = {
        "student_id": "s2",
        "target_school": "school-2",
        "target_class": "10",
        "academic_year": "2026",
        "date_of_birth": "2010-10-01",
        "debts": [],
        "sanctions": [],
        "institution_capacity": {"available": 1},
    }

    resp = auto.request_transfer(req, async_execute=True)
    assert resp["status"] == "scheduled"

    # Local bus processes events synchronously.
    log = read_audit_events()
    assert "transfer_completed" in log or "transfer_executed" in log

    auto.stop()
