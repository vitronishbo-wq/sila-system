from apps.backend.core.routers.router_factory import RouterFactory

from .health import router as health_router

router = RouterFactory.create_health_only_router(
    prefix="/saude", tags=["Saude"], health_router=health_router
)
