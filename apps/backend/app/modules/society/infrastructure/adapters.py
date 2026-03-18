"""Infrastructure adapters for Society module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.society.domain.repositories import ISocietyRepository
SocietyAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Society', repository_interface=ISocietyRepository)
__all__ = ['SocietyAdapter']