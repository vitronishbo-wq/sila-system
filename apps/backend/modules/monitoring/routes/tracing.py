# /opt/sila-system/backend/modules/monitoring/routes/tracing.py

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Path, status

# Inicializa o router. O prefixo será adicionado em monitoring/__init__.py.
router = APIRouter(tags=["Tracing & Distributed Transactions"])

# Simulação de um banco de dados de traços
# Em um sistema real, isso interagiria com Jaeger, Zipkin, ou um backend OpenTelemetry.
MOCK_TRACES_DB = {
    "trace-a1b2c3d4": [
        {"span": "auth_service", "duration_ms": 50, "status": "OK"},
        {"span": "user_db_lookup", "duration_ms": 150, "status": "OK"},
        {"span": "billing_check", "duration_ms": 200, "status": "FAIL"},
    ],
    "trace-e5f6g7h8": [
        {"span": "service_hub_request", "duration_ms": 10, "status": "OK"},
        {"span": "location_service", "duration_ms": 30, "status": "OK"},
    ],
}


@router.get(
    "/traces/{trace_id}",
    summary="Obter detalhes de um Traço Específico",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
async def get_trace_details(
    trace_id: str = Path(
        ..., description="ID único do traço (trace ID) a ser consultado"
    )
):
    """
    Busca e retorna a lista de 'spans' (operações) que compõem um traço.

    Um traço representa a jornada completa de uma requisição através de múltiplos serviços.
    """
    if trace_id not in MOCK_TRACES_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trace ID '{trace_id}' not found.",
        )

    return MOCK_TRACES_DB[trace_id]


@router.get(
    "/traces",
    summary="Listar os traços mais recentes",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
)
async def get_recent_traces():
    """
    Retorna uma lista dos IDs dos traços recentemente capturados.
    """
    return list(MOCK_TRACES_DB.keys())
