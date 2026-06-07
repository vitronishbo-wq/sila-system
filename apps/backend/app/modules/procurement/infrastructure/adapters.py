"""Infrastructure adapters for Procurement module"""

from apps.backend.app.modules.procurement.domain.repositories import IProcurementRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

ProcurementAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Procurement", repository_interface=IProcurementRepository
)
__all__ = ["ProcurementAdapter"]
