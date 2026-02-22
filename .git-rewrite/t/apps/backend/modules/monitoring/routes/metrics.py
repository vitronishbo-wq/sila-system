# /opt/sila-system/backend/modules/monitoring/routes/metrics.py

from fastapi import APIRouter, Response, status
from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest

# O padrão Prometheus/OpenMetrics é o mais comum para métricas em backends modernos.
# Em vez de retornar JSON, este endpoint deve retornar o formato de texto plano do Prometheus.

# Inicializa o router. O prefixo será adicionado em monitoring/__init__.py.
router = APIRouter(tags=["Metrics Collection (Prometheus)"])

# Registro de métricas (CollectorRegistry)
registry = CollectorRegistry()

# ----------------------------------------------------------------------
# Métricas de Exemplo
# ----------------------------------------------------------------------

# 1. Gauge: Uma métrica que pode ir para cima e para baixo (ex: Uso de memória, conexões abertas)
PROCESS_MEMORY = Gauge(
    "process_memory_bytes",
    "Uso de memória do processo Python em bytes",
    registry=registry,
)

# 2. Counter: Uma métrica que só aumenta (ex: Total de requisições, total de erros)
REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total de requisições HTTP recebidas",
    ["method", "endpoint"],  # Labels para segmentação
    registry=registry,
)

# Simulação de atualização de métricas
PROCESS_MEMORY.set(256 * 1024 * 1024)  # 256 MB
REQUESTS_TOTAL.labels("GET", "/health").inc()
REQUESTS_TOTAL.labels("POST", "/data").inc(5)


# ----------------------------------------------------------------------
# Endpoint de Metrics
# ----------------------------------------------------------------------


@router.get(
    "/metrics",
    summary="Endpoint de Coleta de Métricas (Formato Prometheus)",
    status_code=status.HTTP_200_OK,
)
async def get_prometheus_metrics():
    """
    Retorna métricas do sistema e da aplicação no formato OpenMetrics
    para serem raspadas (scraped) por um servidor Prometheus.
    """

    # Gera o formato de texto plano do Prometheus a partir do registro de métricas
    prometheus_data = generate_latest(registry)

    # Retorna o Response com o tipo de conteúdo específico do Prometheus
    return Response(
        content=prometheus_data, media_type="text/plain; version=0.0.4; charset=utf-8"
    )
