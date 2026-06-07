"""API routers for Economy module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Economy", prefix="/economy", tags=["Economy"]
)
__all__ = ["router"]
