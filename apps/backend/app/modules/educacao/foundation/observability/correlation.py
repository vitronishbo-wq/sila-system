from contextvars import ContextVar
from uuid import uuid4

_correlation_id: ContextVar[str] = ContextVar(
    "correlation_id",
    default=""
)


def get_correlation_id() -> str:
    return _correlation_id.get()


def set_correlation_id(value: str) -> None:
    _correlation_id.set(value)


def ensure_correlation_id() -> str:
    current = get_correlation_id()

    if current:
        return current

    new_id = str(uuid4())
    set_correlation_id(new_id)

    return new_id
