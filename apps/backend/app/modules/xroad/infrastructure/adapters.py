"""Infrastructure adapters for Xroad module"""

from apps.backend.app.modules.xroad.domain.repositories import IXroadRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

XroadAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Xroad", repository_interface=IXroadRepository
)
__all__ = ["XroadAdapter"]
