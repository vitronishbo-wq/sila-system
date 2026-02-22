"""
Módulo de métricas para o backend SILA System.
Fornece endpoints para monitoramento com Prometheus.
"""

import os
import time

from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

# Cria o router para as rotas de métricas
router = APIRouter(tags=["metrics"])

# Verifica se as métricas estão habilitadas
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "false").lower() == "true"

# Métricas
REQUEST_COUNT = Counter(
    "sila_http_requests_total",
    "Total de requisições HTTP",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "sila_http_request_duration_seconds",
    "Tempo de resposta das requisições HTTP",
    ["method", "endpoint"],
)

ACTIVE_REQUESTS = Gauge(
    "sila_http_requests_active", "Número de requisições ativas", ["method", "endpoint"]
)


def record_request_metrics(
    method: str, endpoint: str, status_code: int, duration: float
):
    """Registra métricas para uma requisição HTTP."""
    if not ENABLE_METRICS:
        return

    # Remove parâmetros da rota para evitar cardinalidade excessiva
    endpoint = endpoint.split("?")[0].split("{")[0]

    # Incrementa contador de requisições
    REQUEST_COUNT.labels(
        method=method, endpoint=endpoint, http_status=status_code
    ).inc()

    # Registra a latência
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    # Decrementa o contador de requisições ativas
    ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).dec()


def start_request_metrics(method: str, endpoint: str):
    """Inicia o monitoramento de uma requisição HTTP."""
    if not ENABLE_METRICS:
        return

    endpoint = endpoint.split("?")[0].split("{")[0]
    ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).inc()
    return time.time()


@router.get("/metrics", response_class=PlainTextResponse)
async def get_metrics():
    """Endpoint para o Prometheus coletar métricas."""
    if not ENABLE_METRICS:
        return Response("Métricas desativadas", status_code=404)

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Middleware para monitorar requisições HTTP
class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not ENABLE_METRICS:
            return await self.app(scope, receive, send)

        method = scope["method"]
        path = scope.get("path", "")

        # Ignora requisições para o endpoint de métricas
        if path == "/metrics":
            return await self.app(scope, receive, send)

        start_time = time.time()

        # Incrementa contador de requisições ativas
        start_request_metrics(method, path)

        # Captura a resposta
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                # Registra as métricas quando a resposta é enviada
                duration = time.time() - start_time
                record_request_metrics(method, path, status_code, duration)

            await send(message)

        try:
            return await self.app(scope, receive, send_wrapper)
        except Exception as e:
            # Registra erros nas métricas
            if ENABLE_METRICS:
                duration = time.time() - start_time
                record_request_metrics(method, path, 500, duration)
            raise
