"""API routers for Industry module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Industry", prefix="/industry", tags=["Industry"]
)
__all__ = ["router"]
