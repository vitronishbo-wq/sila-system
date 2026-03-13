from __future__ import annotations
import time
from collections.abc import Callable

def retry(call: Callable, attempts: int=3, wait_seconds: float=0.1):
    last_error = None
    for _ in range(attempts):
        try:
            return call()
        except Exception as exc:
            last_error = exc
            time.sleep(wait_seconds)
    if last_error is not None:
        raise last_error