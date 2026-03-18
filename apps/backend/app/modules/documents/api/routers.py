"""API routers for Documents module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Documents', prefix='/documents', tags=['Documents'])
__all__ = ['router']