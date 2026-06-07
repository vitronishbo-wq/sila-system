"""Audit middleware for FastAPI"""

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .audit_engine import AuditAction, get_audit_engine


class AuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.audit_engine = get_audit_engine()

    async def dispatch(self, request: Request, call_next):
        # Skip audit for health/docs
        if any(request.url.path.startswith(p) for p in ["/health", "/docs", "/openapi"]):
            return await call_next(request)

        # Extract module and action
        parts = request.url.path.strip("/").split("/")
        module = parts[1] if len(parts) > 1 else "unknown"
        method_map = {
            "GET": AuditAction.READ,
            "POST": AuditAction.CREATE,
            "PUT": AuditAction.UPDATE,
            "DELETE": AuditAction.DELETE,
        }
        action = method_map.get(request.method, AuditAction.READ)

        # Initiate audit
        audit_record = await self.audit_engine.initiate(
            user_id="unknown",
            module=module,
            action=action,
            request_path=str(request.url.path),
            request_method=request.method,
        )
        request.state.audit_id = audit_record.audit_id

        try:
            response = await call_next(request)
            await self.audit_engine.complete(
                audit_record.audit_id, result_code=response.status_code
            )
            return response
        except Exception as e:
            await self.audit_engine.fail(
                audit_record.audit_id, error_code=500, error_message=str(e)
            )
            raise


def setup_audit_middleware(app: FastAPI) -> None:
    app.add_middleware(AuditMiddleware)
