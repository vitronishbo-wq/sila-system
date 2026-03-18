"""API routers for MigrationService module"""
from apps.backend.core.routers.router_factory import RouterFactory
router = RouterFactory.create_module_router(module_name='MigrationService', prefix='/migration_service', tags=['MigrationService'])
__all__ = ['router']