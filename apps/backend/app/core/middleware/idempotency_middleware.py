from __future__ import annotations

from collections.abc import Iterable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class IdempotencyMiddleware(BaseHTTPMiddleware):
    """Middleware that enforces presence of Idempotency-Key header for critical routes.

    Configuration:
    - `PROTECTED_PATH_PREFIXES` env var (comma-separated) can define additional protected prefixes.

    Default protected paths:
    - /api/v1/educacao/matriculas
    - /api/v1/educacao/transferencias
    """

    DEFAULT_PROTECTED_PREFIXES = (
        "/api/v1/educacao/matriculas",
        "/api/v1/educacao/transferencias",
    )

    def __init__(self, app, protected_prefixes: Iterable[str] | None = None):
        super().__init__(app)
        self.protected_prefixes = tuple(protected_prefixes) if protected_prefixes else self.DEFAULT_PROTECTED_PREFIXES

    @staticmethod
    def _has_idempotency(headers) -> bool:
        for name, value in headers:
            if name.decode().lower() == "idempotency-key" and value.strip():
                return True
        return False

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method.upper()

        # Only enforce for POST/PUT/DELETE on protected prefixes
        if method in ("POST", "PUT", "DELETE") and any(path.startswith(p) for p in self.protected_prefixes):
            if not self._has_idempotency(request.scope.get("headers", [])):
                return JSONResponse(
                    {"detail": "Idempotency-Key header is required for this operation."},
                    status_code=400,
                )
        return await call_next(request)
