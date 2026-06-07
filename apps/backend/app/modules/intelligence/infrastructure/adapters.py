"""Infrastructure adapters for Intelligence module"""

from apps.backend.app.modules.intelligence.domain.repositories import IIntelligenceRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

IntelligenceAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Intelligence", repository_interface=IIntelligenceRepository
)
__all__ = ["IntelligenceAdapter"]
