from fastapi import APIRouter
from apps.backend.app.modules.infrastructure_sector.meteorologia.api.endpoints import estacoes_router, observacoes_router
router = APIRouter(prefix='/meteorologia', tags=['Meteorologia'])
router.include_router(estacoes_router)
router.include_router(observacoes_router)