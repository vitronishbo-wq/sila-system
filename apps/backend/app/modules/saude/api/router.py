from fastapi import APIRouter
from apps.backend.app.modules.saude.api.health import router as health_router
from apps.backend.app.modules.saude.api.v1.endpoints import router as v1_router

router = APIRouter(prefix="/saude", tags=["Saude"])

router.include_router(health_router)
router.include_router(v1_router, prefix="/v1")
