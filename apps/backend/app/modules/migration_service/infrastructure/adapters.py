"""Infrastructure adapters for MigrationService module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.migration_service.domain.repositories import IMigrationServiceRepository
MigrationServiceAdapter = AdapterFactory.create_infrastructure_adapter(module_name='MigrationService', repository_interface=IMigrationServiceRepository)
__all__ = ['MigrationServiceAdapter']