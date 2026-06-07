import os
import time
from pathlib import Path

from foundation.orchestration.orchestrator import Orchestrator


def test_retry_and_dlq_written():
    orch = Orchestrator()
    # ensure DLQ file is removed before test
    if orch.DLQ_PATH.exists():
        try:
            orch.DLQ_PATH.unlink()
        except Exception:
            pass

    orch.start()

    # define a task that always fails
    def failing_task(x):
        raise RuntimeError("intentional failure")

    # submit with 2 retries (so attempts = 3 total: initial + 2 retries)
    orch.submit(failing_task, 1, max_retries=2)

    # wait enough time for retries and backoff: 0.5 + 1.0 + small buffer
    time.sleep(3.0)

    dlq = orch.get_dlq()
    orch.stop()

    assert len(dlq) >= 1
    entry = dlq[0]
    assert "intentional failure" in entry.get("error") or "failing_task" in entry.get("func")

    # verify DLQ file exists and contains an entry
    assert orch.DLQ_PATH.exists()
    text = orch.DLQ_PATH.read_text(encoding="utf-8")
    assert "intentional failure" in text or "failing_task" in text
