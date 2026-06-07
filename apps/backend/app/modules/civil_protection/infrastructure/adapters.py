"""Infrastructure adapters for CivilProtection module"""

from apps.backend.app.modules.civil_protection.domain.repositories import ICivilProtectionRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

CivilProtectionAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="CivilProtection", repository_interface=ICivilProtectionRepository
)
__all__ = ["CivilProtectionAdapter"]
