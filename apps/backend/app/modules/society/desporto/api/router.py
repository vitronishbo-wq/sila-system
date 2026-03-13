from fastapi import APIRouter
from app.modules.society.desporto.api.endpoints import atletas_router, clubes_router, competicoes_router, estadios_router, jogos_router
router = APIRouter(prefix='/desporto', tags=['Desporto'])
router.include_router(atletas_router)
router.include_router(competicoes_router)
router.include_router(clubes_router)
router.include_router(jogos_router)
router.include_router(estadios_router)