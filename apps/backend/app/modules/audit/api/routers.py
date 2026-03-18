"""API routers for Audit module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Audit', prefix='/audit', tags=['Audit'])
__all__ = ['router']