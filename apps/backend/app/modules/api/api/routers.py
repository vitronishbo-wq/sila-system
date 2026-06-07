"""API routers for Api module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(module_name="Api", prefix="/api", tags=["Api"])
__all__ = ["router"]
