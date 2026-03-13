from fastapi import APIRouter
from app.modules.industry.api.endpoints import catalogos_router, estabelecimentos_industriais_router
router = APIRouter(prefix='/industria', tags=['Industria'])
router.include_router(catalogos_router)
router.include_router(estabelecimentos_industriais_router)
