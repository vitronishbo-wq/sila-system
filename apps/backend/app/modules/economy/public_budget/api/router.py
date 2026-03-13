from fastapi import APIRouter
from .health import router as health_router
router = APIRouter(prefix='/budget', tags=['Public Budget'])
router.include_router(health_router)