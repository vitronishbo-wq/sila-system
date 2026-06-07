"""API routers for Educacao module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Educacao", prefix="/educacao", tags=["Educacao"]
)
__all__ = ["router"]
