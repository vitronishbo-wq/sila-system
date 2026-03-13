from fastapi import APIRouter
from apps.backend.app.modules.civil_protection.api.endpoints import atendimentos_router, bombeiros_router, corporacoes_router, despachos_router, ocorrencias_emergenciais_router
router = APIRouter(prefix='/protecao-civil', tags=['Protecao Civil'])
router.include_router(corporacoes_router)
router.include_router(bombeiros_router)
router.include_router(ocorrencias_emergenciais_router)
router.include_router(despachos_router)
router.include_router(atendimentos_router)