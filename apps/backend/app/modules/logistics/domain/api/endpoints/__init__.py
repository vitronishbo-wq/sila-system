from apps.backend.app.modules.logistics.api.endpoints.analytics import router as analytics_router
from apps.backend.app.modules.logistics.api.endpoints.bilhetagem import router as bilhetagem_router
from apps.backend.app.modules.logistics.api.endpoints.frotas import router as frotas_router
from apps.backend.app.modules.logistics.api.endpoints.linhas import router as linhas_router
from apps.backend.app.modules.logistics.api.endpoints.viagens import router as viagens_router
__all__ = ['viagens_router', 'frotas_router', 'linhas_router', 'bilhetagem_router', 'analytics_router']
