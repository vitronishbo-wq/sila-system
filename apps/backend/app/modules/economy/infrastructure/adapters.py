"""Infrastructure adapters for Economy module"""

from apps.backend.app.modules.economy.domain.repositories import IEconomyRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

EconomyAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Economy", repository_interface=IEconomyRepository
)
__all__ = ["EconomyAdapter"]
