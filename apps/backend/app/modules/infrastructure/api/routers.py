"""API routers for Infrastructure module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Infrastructure', prefix='/infrastructure', tags=['Infrastructure'])
__all__ = ['router']