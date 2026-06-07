"""API routers for Xroad module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(module_name="Xroad", prefix="/xroad", tags=["Xroad"])
__all__ = ["router"]
