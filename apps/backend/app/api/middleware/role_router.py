from __future__ import annotations
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class RoleBasedRoutingMiddleware(BaseHTTPMiddleware):
    """No-op compatibility middleware for legacy bootstrap path."""

    async def dispatch(self, request: Request, call_next) -> Response:
        return await call_next(request)