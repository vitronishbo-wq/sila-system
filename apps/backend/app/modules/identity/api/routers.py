"""API routers for Identity module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Identity', prefix='/identity', tags=['Identity'])
__all__ = ['router']