from fastapi import APIRouter
from app.modules.economy.trade.services.api.endpoints import catalogos_router, estabelecimentos_comerciais_router
router = APIRouter(prefix='/comercio_servicos', tags=['Comercio Servicos'])
router.include_router(catalogos_router)
router.include_router(estabelecimentos_comerciais_router)