"""Infrastructure adapters for Api module"""

from apps.backend.app.modules.api.domain.repositories import IApiRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

ApiAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Api", repository_interface=IApiRepository
)
__all__ = ["ApiAdapter"]
