import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def trace_operation(name: str):

    def wrapper(func):

        if hasattr(func, "__call__"):
            @wraps(func)
            async def inner(*args, **kwargs):

                started = time.perf_counter()

                try:
                    result = await func(*args, **kwargs)

                    elapsed = time.perf_counter() - started

                    logger.info(
                        "operation_completed",
                        extra={
                            "operation": name,
                            "duration": elapsed,
                        }
                    )

                    return result

                except Exception:

                    elapsed = time.perf_counter() - started

                    logger.exception(
                        "operation_failed",
                        extra={
                            "operation": name,
                            "duration": elapsed,
                        }
                    )

                    raise

            return inner

        return func

    return wrapper
