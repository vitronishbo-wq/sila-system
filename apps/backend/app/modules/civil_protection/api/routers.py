"""API routers for CivilProtection module"""

from apps.backend.core.routers.router_factory import RouterFactory

router = RouterFactory.create_module_router(
    module_name="CivilProtection", prefix="/civil_protection", tags=["CivilProtection"]
)
__all__ = ["router"]
