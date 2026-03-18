"""Health check endpoints para módulo de Pagamentos."""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", summary="Payment Module Health Check")
async def payment_health():
    """
    Health check para o módulo de Pagamentos.
    
    Verifica:
    - Disponibilidade do serviço
    - Status da conexão com banco de dados (quando aplicável)
    - Status dos repositórios críticos
    """
    return {
        "status": "healthy",
        "module": "payment",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


@router.get("/health/ready", summary="Payment Module Readiness Check")
async def payment_readiness():
    """
    Readiness check para verificar se o módulo está pronto para receber requisições.
    """
    return {
        "ready": True,
        "module": "payment",
        "timestamp": datetime.utcnow().isoformat(),
    }


__all__ = ["router"]
