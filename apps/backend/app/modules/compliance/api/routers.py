"""API routers for Compliance module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Compliance", prefix="/compliance", tags=["Compliance"]
)
__all__ = ["router"]
