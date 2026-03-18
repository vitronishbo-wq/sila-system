from fastapi import APIRouter
from apps.backend.app.modules.energy.api.endpoints import central_geradora_router, consumo_router, faturas_router, geracao_router, linha_transmissao_router, subestacao_router, usinas_router
router = APIRouter(prefix='/energia', tags=['Energia'])
router.include_router(usinas_router)
router.include_router(central_geradora_router)
router.include_router(subestacao_router)
router.include_router(linha_transmissao_router)
router.include_router(geracao_router)
router.include_router(consumo_router)
router.include_router(faturas_router)