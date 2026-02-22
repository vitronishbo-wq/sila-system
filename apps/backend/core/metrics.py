from fastapi import FastAPI, Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CollectorRegistry,
    ProcessCollector,
    GCCollector,
    CONTENT_TYPE_LATEST,
)
import time
import logging
from functools import wraps

# Create a registry for metrics
registry = CollectorRegistry()

# Flag to ensure ProcessCollector is registered only once
_process_collector_registered = False

if not _process_collector_registered:
    try:
        registry.register(ProcessCollector())
        _process_collector_registered = True
    except ValueError:
        # Already registered, skip
        pass

# Flag to ensure GCCollector is registered only once
_gc_collector_registered = False

if not _gc_collector_registered:
    try:
        registry.register(GCCollector())
        _gc_collector_registered = True
    except ValueError:
        # Already registered, skip
        pass

# Define metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
    registry=registry,
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    registry=registry,
)
ACTIVE_USERS = Counter("active_users_total", "Total active users", registry=registry)
ERROR_COUNT = Counter(
    "errors_total", "Total errors", ["endpoint", "error_type"], registry=registry
)

logger = logging.getLogger(__name__)


def metrics_middleware(app: FastAPI):
    """Middleware para coletar métricas HTTP"""

    @app.middleware("http")
    async def prometheus_middleware(request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Record metrics
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code,
            ).inc()

            REQUEST_DURATION.labels(
                method=request.method, endpoint=request.url.path
            ).observe(process_time)

            return response
        except Exception as e:
            process_time = time.time() - start_time
            REQUEST_DURATION.labels(
                method=request.method, endpoint=request.url.path
            ).observe(process_time)

            # Log error and increment error counter
            logger.error(f"Error in {request.method} {request.url.path}: {str(e)}")
            ERROR_COUNT.labels(
                endpoint=request.url.path, error_type=type(e).__name__
            ).inc()
            raise

    return app


def get_metrics():
    """Expose Prometheus metrics."""
    return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)


def track_user_activity(user_id: str):
    """Track active users"""
    ACTIVE_USERS.labels(user_id=user_id).inc()


def track_error(endpoint: str, error_type: str):
    """Track errors"""
    ERROR_COUNT.labels(endpoint=endpoint, error_type=error_type).inc()
