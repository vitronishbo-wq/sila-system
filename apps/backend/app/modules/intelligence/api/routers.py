"""API routers for Intelligence module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Intelligence', prefix='/intelligence', tags=['Intelligence'])
__all__ = ['router']