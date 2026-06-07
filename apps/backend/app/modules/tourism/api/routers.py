"""API routers for Tourism module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Tourism", prefix="/tourism", tags=["Tourism"]
)
__all__ = ["router"]
