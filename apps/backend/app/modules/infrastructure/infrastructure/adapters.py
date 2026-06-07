"""Infrastructure adapters for Infrastructure module"""

from apps.backend.app.modules.infrastructure.domain.repositories import IInfrastructureRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

InfrastructureAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Infrastructure", repository_interface=IInfrastructureRepository
)
__all__ = ["InfrastructureAdapter"]
