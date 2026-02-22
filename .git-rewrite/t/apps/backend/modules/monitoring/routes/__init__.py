# /opt/sila-system/backend/modules/monitoring/routes/__init__.py

# Routes package initialization

# Importa os APIRouters definidos em cada módulo de rota.
# Estes são importados aqui e depois exportados através do __all__.
from fastapi import APIRouter
from .health import router as health_router
from .metrics import router as metrics_router
from .tracing import router as tracing_router

# Router principal que consolida todas as rotas de monitoring
router = APIRouter(tags=["Monitoring & Observability"])

# Incluir todas as rotas específicas
router.include_router(health_router)
router.include_router(metrics_router)
router.include_router(tracing_router)


# Health check endpoint
@router.get("/ping")
async def ping():
    """Health check para o módulo monitoring"""
    return {"status": "ok", "module": "monitoring"}


# A lista __all__ define o que será exportado quando
# alguém fizer um 'from modules.monitoring.routes import *'
# ou quando o módulo pai (monitoring/__init__.py) fizer
# 'from .routes import router as monitoring_router' (dependendo da lógica)
__all__ = ["router", "health_router", "metrics_router", "tracing_router"]
