"""Infrastructure adapters for Justice module"""

from apps.backend.app.modules.justice.domain.repositories import IJusticeRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

JusticeAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Justice", repository_interface=IJusticeRepository
)
__all__ = ["JusticeAdapter"]
