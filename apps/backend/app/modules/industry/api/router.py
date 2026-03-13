from fastapi import APIRouter
from .endpoints import catalogos_router, estabelecimentos_industriais_router
from .health import router as health_router

router = APIRouter(prefix="/industria", tags=["Industria"])
router.include_router(health_router)
router.include_router(catalogos_router)
router.include_router(estabelecimentos_industriais_router)
