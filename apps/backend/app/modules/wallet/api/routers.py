"""API routers for Wallet module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(module_name="Wallet", prefix="/wallet", tags=["Wallet"])
__all__ = ["router"]
