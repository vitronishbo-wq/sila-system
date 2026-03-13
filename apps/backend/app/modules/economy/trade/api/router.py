from fastapi import APIRouter
from app.modules.economy.trade.external.api.router import router as external_router
from app.modules.economy.trade.services.api.router import router as services_router
router = APIRouter(tags=['Trade'])
router.include_router(external_router)
router.include_router(services_router)