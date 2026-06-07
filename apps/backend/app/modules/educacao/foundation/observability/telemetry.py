from .correlation import get_correlation_id
from .metrics import HTTP_LATENCY, HTTP_REQUESTS


def record_http_request(method: str, endpoint: str, status: str, duration: float):
    HTTP_REQUESTS.labels(method=method, endpoint=endpoint, status=status).inc()
    HTTP_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)


def current_correlation():
    return get_correlation_id()
