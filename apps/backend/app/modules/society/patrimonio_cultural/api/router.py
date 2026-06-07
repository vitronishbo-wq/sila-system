from fastapi import APIRouter

from apps.backend.app.modules.society.patrimonio_cultural.api.endpoints import assets_router

router = APIRouter(prefix="/patrimonio-cultural", tags=["Patrimonio Cultural"])
router.include_router(assets_router)
