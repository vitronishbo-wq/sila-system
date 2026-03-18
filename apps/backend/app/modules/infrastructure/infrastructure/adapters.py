"""Infrastructure adapters for Infrastructure module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.infrastructure.domain.repositories import IInfrastructureRepository
InfrastructureAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Infrastructure', repository_interface=IInfrastructureRepository)
__all__ = ['InfrastructureAdapter']