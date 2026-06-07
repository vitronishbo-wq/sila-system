import json
import queue
import threading
import time
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import Any

from foundation.orchestration.dlq import (
    DeadLetterQueue,
    build_dead_letter_queue,
)


class Orchestrator:
    """In-memory orchestrator with retries and pluggable DLQ support.

    Tasks are enqueued as tuples and on failure are retried up to
    `max_retries` times with exponential backoff. Failed tasks beyond
    retries are published to a real dead letter queue when configured.
    """

    DLQ_PATH = Path("reports") / "orchestrator_dlq.log"

    def __init__(self, dlq: DeadLetterQueue | None = None):
        self._q = queue.Queue()
        self._worker = None
        self._stop_event = threading.Event()
        self._dlq_entries = []
        self._dlq = dlq or build_dead_letter_queue()
        self.DLQ_PATH.parent.mkdir(parents=True, exist_ok=True)

    def start(self):
        if self._worker and self._worker.is_alive():
            return

        self._stop_event.clear()
        self._worker = threading.Thread(target=self._run_loop, daemon=True)
        self._worker.start()

    def stop(self, timeout: float = 1.0):
        self._stop_event.set()
        if self._worker:
            self._worker.join(timeout=timeout)

    def _run_loop(self):
        while not self._stop_event.is_set():
            try:
                task = self._q.get(timeout=0.5)
            except queue.Empty:
                continue

            func = task.get("func")
            args = task.get("args", ())
            kwargs = task.get("kwargs", {})
            attempts = task.get("attempts", 0)
            max_retries = task.get("max_retries", 0)

            try:
                func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                if attempts <= max_retries:
                    backoff = 0.5 * (2 ** (attempts - 1))
                    time.sleep(backoff)
                    self._q.put({"func": func, "args": args, "kwargs": kwargs, "attempts": attempts, "max_retries": max_retries})
                else:
                    tb = traceback.format_exc()
                    entry = {"func": getattr(func, "__name__", str(func)), "args": repr(args), "kwargs": repr(kwargs), "error": str(e), "traceback": tb}
                    self._dlq_entries.append(entry)
                    try:
                        self._dlq.record(entry)
                    except Exception:
                        try:
                            with open(self.DLQ_PATH, "a", encoding="utf-8") as f:
                                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                        except Exception:
                            pass

    def submit(self, func: Callable, *args: Any, max_retries: int | None = 0, **kwargs: Any) -> None:
        """Submit a task with optional `max_retries`.

        Example: submit(fn, arg1, arg2, max_retries=3, kw1=val)
        """
        task = {"func": func, "args": args, "kwargs": kwargs, "attempts": 0, "max_retries": int(max_retries or 0)}
        self._q.put(task)

    def get_dlq(self):
        return list(self._dlq_entries)
