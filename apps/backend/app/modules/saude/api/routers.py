"""API routers for Saude module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Saude', prefix='/saude', tags=['Saude'])
__all__ = ['router']