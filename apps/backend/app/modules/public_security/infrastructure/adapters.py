"""Infrastructure adapters for PublicSecurity module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.public_security.domain.repositories import IPublicSecurityRepository
PublicSecurityAdapter = AdapterFactory.create_infrastructure_adapter(module_name='PublicSecurity', repository_interface=IPublicSecurityRepository)
__all__ = ['PublicSecurityAdapter']