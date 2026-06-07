from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class RequestContext:
    correlation_id: str
    actor_id: str | None = None
    tenant_id: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None


_context: ContextVar[RequestContext | None] = ContextVar(
    "request_context",
    default=None,
)


def set_request_context(ctx: RequestContext):
    _context.set(ctx)


def get_request_context() -> RequestContext | None:
    return _context.get()
