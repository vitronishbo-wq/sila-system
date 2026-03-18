from fastapi import APIRouter
from apps.backend.app.modules.logistics.api.endpoints import analytics_router, bilhetagem_router, frotas_router, linhas_router, viagens_router
router = APIRouter(prefix='/transportes-logistica', tags=['Transportes Logistica'])
router.include_router(viagens_router)
router.include_router(frotas_router)
router.include_router(linhas_router)
router.include_router(bilhetagem_router)
router.include_router(analytics_router)