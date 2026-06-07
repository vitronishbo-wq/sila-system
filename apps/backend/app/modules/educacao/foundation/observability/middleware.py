import os
from collections.abc import Callable
from time import perf_counter
from uuid import uuid4

from apps.backend.app.core.settings import settings
from starlette.middleware.base import BaseHTTPMiddleware

from .context import RequestContext, set_request_context
from .correlation import set_correlation_id
from .metrics import HTTP_LATENCY, HTTP_REQUESTS


class ObservabilityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        correlation_id = (
            request.headers.get("X-Correlation-ID")
            or str(uuid4())
        )

        set_correlation_id(correlation_id)

        ctx = RequestContext(
            correlation_id=correlation_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        set_request_context(ctx)

        response = await call_next(request)

        response.headers["X-Correlation-ID"] = correlation_id

        return response


class ASGIMetricsMiddleware(BaseHTTPMiddleware):
    """Starlette/ASGI middleware to collect Prometheus metrics for HTTP requests."""

    async def dispatch(self, request, call_next: Callable):
        path = request.url.path
        # skip metrics for health, metrics, docs and static assets to avoid high-cardinality/noise
        DEFAULT_EXCLUDE_PATHS = (
            "/metrics",
            "/api/health",
            "/system/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/static",
            "/favicon.ico",
        )

        env_name = getattr(settings, "OBS_EXCLUDE_PATHS_ENV_NAME", "OBS_EXCLUDE_PATHS")
        raw = os.getenv(env_name)
        if raw:
            # allow comma-separated list in env var (e.g. "/metrics,/api/health")
            EXCLUDE_PATHS = tuple(p.strip() for p in raw.split(",") if p.strip())
        else:
            EXCLUDE_PATHS = DEFAULT_EXCLUDE_PATHS

        if any(path.startswith(p) for p in EXCLUDE_PATHS):
            return await call_next(request)

        method = request.method
        # prefer resolved route path when available (helps reduce cardinality)
        endpoint = getattr(request.scope.get("route"), "path", request.url.path)
        start = perf_counter()
        response = await call_next(request)
        elapsed = perf_counter() - start

        status = str(response.status_code)
        try:
            HTTP_REQUESTS.labels(method=method, endpoint=endpoint, status=status).inc()
            HTTP_LATENCY.labels(method=method, endpoint=endpoint).observe(elapsed)
        except Exception:
            # protect the request path from metric errors
            pass

        return response
