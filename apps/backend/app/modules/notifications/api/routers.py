"""API routers for Notifications module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Notifications', prefix='/notifications', tags=['Notifications'])
__all__ = ['router']