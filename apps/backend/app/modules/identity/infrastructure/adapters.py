"""Infrastructure adapters for Identity module"""

from apps.backend.app.modules.identity.domain.repositories import IIdentityRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

IdentityAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Identity", repository_interface=IIdentityRepository
)
__all__ = ["IdentityAdapter"]
