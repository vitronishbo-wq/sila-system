"""API routers for Operations module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Operations", prefix="/operations", tags=["Operations"]
)
__all__ = ["router"]
