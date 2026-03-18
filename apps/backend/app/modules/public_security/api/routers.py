"""API routers for PublicSecurity module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='PublicSecurity', prefix='/public_security', tags=['PublicSecurity'])
__all__ = ['router']