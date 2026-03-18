"""Infrastructure adapters for CivilProtection module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.civil_protection.domain.repositories import ICivilProtectionRepository
CivilProtectionAdapter = AdapterFactory.create_infrastructure_adapter(module_name='CivilProtection', repository_interface=ICivilProtectionRepository)
__all__ = ['CivilProtectionAdapter']