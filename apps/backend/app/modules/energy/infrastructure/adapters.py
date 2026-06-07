"""Infrastructure adapters for Energy module"""

from apps.backend.app.modules.energy.domain.repositories import IEnergyRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

EnergyAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Energy", repository_interface=IEnergyRepository
)
__all__ = ["EnergyAdapter"]
