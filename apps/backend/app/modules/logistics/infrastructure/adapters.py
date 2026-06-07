"""Infrastructure adapters for Logistics module"""

from apps.backend.app.modules.logistics.domain.repositories import ILogisticsRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

LogisticsAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Logistics", repository_interface=ILogisticsRepository
)
__all__ = ["LogisticsAdapter"]
