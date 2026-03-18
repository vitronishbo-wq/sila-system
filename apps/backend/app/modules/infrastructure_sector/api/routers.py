"""API routers for InfrastructureSector module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='InfrastructureSector', prefix='/infrastructure_sector', tags=['InfrastructureSector'])
__all__ = ['router']