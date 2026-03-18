from apps.backend.core.routers.router_factory import RouterFactory
from .health import router as health_router
from .endpoints.qr import router as qr_router
router = RouterFactory.create_health_only_router(prefix='/identity', tags=['endpoints'], health_router=health_router)
router.include_router(qr_router)
