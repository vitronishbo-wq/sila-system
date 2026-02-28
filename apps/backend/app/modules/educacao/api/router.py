from fastapi import APIRouter
from app.modules.educacao.api.endpoints import inscricoes_router, matricula_router

router = APIRouter(prefix="/educacao", tags=["Educacao"])
router.include_router(matricula_router)
router.include_router(inscricoes_router)
