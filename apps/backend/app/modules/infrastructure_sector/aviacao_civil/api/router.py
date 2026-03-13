from fastapi import APIRouter
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.api.endpoints import aeronaves_router, ocorrencias_router, voos_router
router = APIRouter(prefix='/aviacao-civil', tags=['Aviacao Civil'])
router.include_router(aeronaves_router)
router.include_router(voos_router)
router.include_router(ocorrencias_router)