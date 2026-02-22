# /opt/sila-system/backend/modules/monitoring/routes/health.py (MANTIDO)

from typing import Any, Dict

from fastapi import APIRouter, Response, status

# Inicializa o router. O prefixo será adicionado pelo módulo pai (__init__.py)
router = APIRouter(tags=["Health Checks"])


# --- Health Check (Liveness) ---
@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Verificação de Liveness (Atividade)",
    response_model=Dict[str, Any],
)
async def get_liveness_status():
    """
    Endpoint de Liveness. Indica se a aplicação está **executando**.
    """
    return {
        "status": "UP",
        "service": "SILA Monitoring Module",
        "details": {
            "liveness_check": "passed",
        },
    }


# --- Readiness Check (Prontidão) ---
@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Verificação de Readiness (Prontidão)",
    response_description="Status OK se o serviço estiver pronto para receber tráfego",
)
async def get_readiness_status(response: Response):
    """
    Endpoint de Readiness. Indica se a aplicação está **pronta** para receber tráfego.
    """
    try:
        # Simula a verificação de dependências críticas (DB, Message Queue, etc.)
        is_db_connected = True
        is_mq_ready = True

        if not is_db_connected or not is_mq_ready:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {
                "status": "DOWN",
                "error": "One or more critical dependencies failed",
            }

        return {"status": "READY", "details": {"database": "OK", "message_queue": "OK"}}

    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "DOWN", "error": f"Readiness check failed: {e}"}
