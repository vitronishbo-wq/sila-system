"""Observability utilities for educacao.foundation.

Provides correlation id, request context, logging, metrics, tracing and
health check primitives used across the module.
"""

from .context import RequestContext, get_request_context, set_request_context
from .correlation import ensure_correlation_id, get_correlation_id, set_correlation_id
from .decorators import trace_operation
from .health import HealthStatus, check_database, check_eventbus
from .logging import CorrelationFilter, configure_logging
from .metrics import HTTP_LATENCY, HTTP_REQUESTS

__all__ = [
    "ensure_correlation_id",
    "get_correlation_id",
    "set_correlation_id",
    "RequestContext",
    "set_request_context",
    "get_request_context",
    "configure_logging",
    "CorrelationFilter",
    "HTTP_REQUESTS",
    "HTTP_LATENCY",
    "trace_operation",
    "HealthStatus",
    "check_database",
    "check_eventbus",
]
