from fastapi import APIRouter
from .birth_routes import router as birth_router
from .death_routes import router as death_router
from .marriage_routes import router as marriage_router
router = APIRouter(prefix='/vital-events', tags=['justice:vital-events'])
router.include_router(birth_router)
router.include_router(death_router)
router.include_router(marriage_router)