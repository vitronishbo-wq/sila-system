from fastapi import APIRouter
from app.modules.infrastructure.api.endpoints import dashboard_router, editais_router, licitacoes_router, obras_router, projetos_router
router = APIRouter(prefix='/obras-publicas', tags=['Obras Publicas'])
router.include_router(dashboard_router)
router.include_router(obras_router)
router.include_router(projetos_router)
router.include_router(licitacoes_router)
router.include_router(editais_router)
