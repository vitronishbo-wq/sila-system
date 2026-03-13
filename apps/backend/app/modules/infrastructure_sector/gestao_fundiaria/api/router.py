from fastapi import APIRouter
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints import desapropriacoes_router, georreferenciamentos_router, imoveis_router, matriculas_router, oneracoes_router, proprietarios_router
router = APIRouter(prefix='/gestao-fundiaria', tags=['Gestao Fundiaria'])
router.include_router(imoveis_router)
router.include_router(proprietarios_router)
router.include_router(oneracoes_router)
router.include_router(desapropriacoes_router)
router.include_router(matriculas_router)
router.include_router(georreferenciamentos_router)