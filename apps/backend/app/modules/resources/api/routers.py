"""API routers for Resources module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Resources", prefix="/resources", tags=["Resources"]
)
__all__ = ["router"]
