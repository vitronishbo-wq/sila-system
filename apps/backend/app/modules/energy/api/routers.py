"""API routers for Energy module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(module_name="Energy", prefix="/energy", tags=["Energy"])
__all__ = ["router"]
