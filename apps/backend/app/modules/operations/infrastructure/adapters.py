"""Infrastructure adapters for Operations module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.operations.domain.repositories import IOperationsRepository
OperationsAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Operations', repository_interface=IOperationsRepository)
__all__ = ['OperationsAdapter']