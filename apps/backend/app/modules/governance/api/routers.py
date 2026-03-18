"""API routers for Governance module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='Governance', prefix='/governance', tags=['Governance'])
__all__ = ['router']