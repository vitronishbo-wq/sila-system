"""Infrastructure adapters for InfrastructureSector module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.infrastructure_sector.domain.repositories import IInfrastructureSectorRepository
InfrastructureSectorAdapter = AdapterFactory.create_infrastructure_adapter(module_name='InfrastructureSector', repository_interface=IInfrastructureSectorRepository)
__all__ = ['InfrastructureSectorAdapter']