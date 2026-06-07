from fastapi import APIRouter

from apps.backend.app.modules.governance.cooperacao_internacional.api.endpoints import (
    acordos_router,
    projetos_router,
    vistos_router,
)

router = APIRouter(prefix="/cooperacao-internacional", tags=["Cooperacao Internacional"])
router.include_router(acordos_router)
router.include_router(projetos_router)
router.include_router(vistos_router)
