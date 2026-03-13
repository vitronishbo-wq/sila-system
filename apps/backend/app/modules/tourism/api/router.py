from fastapi import APIRouter
from .health import router as health_router

router = APIRouter(prefix="/tourism", tags=["Tourism"])
router.include_router(health_router)
