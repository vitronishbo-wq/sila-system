from fastapi import APIRouter
from app.modules.intelligence.ciencia_pesquisa.api.endpoints import instituicoes_router, pesquisadores_router, projetos_router
router = APIRouter(prefix='/ciencia-pesquisa', tags=['Ciencia Pesquisa'])
router.include_router(instituicoes_router)
router.include_router(pesquisadores_router)
router.include_router(projetos_router)