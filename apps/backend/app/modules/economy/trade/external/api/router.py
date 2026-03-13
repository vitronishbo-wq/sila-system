from fastapi import APIRouter
from apps.backend.app.modules.economy.trade.external.api.endpoints import get_endpoint_routers
router = APIRouter(prefix='/comercio_externo', tags=['Comercio Externo'])
for endpoint_router in get_endpoint_routers():
    router.include_router(endpoint_router)