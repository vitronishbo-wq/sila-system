"""API routers for Society module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Society", prefix="/society", tags=["Society"]
)
__all__ = ["router"]
