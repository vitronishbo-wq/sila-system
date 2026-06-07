from apps.backend.core.routers.router_factory import RouterFactory

from .health import router as health_router

router = RouterFactory.create_health_only_router(
    prefix="/generation", tags=["endpoints"], health_router=health_router
)
