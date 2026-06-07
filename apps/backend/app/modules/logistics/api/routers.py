"""API routers for Logistics module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="Logistics", prefix="/logistics", tags=["Logistics"]
)
__all__ = ["router"]
