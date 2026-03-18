"""API routers for Justice module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Justice', prefix='/justice', tags=['Justice'])
__all__ = ['router']