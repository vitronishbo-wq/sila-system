"""Infrastructure adapters for Resources module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.resources.domain.repositories import IResourcesRepository
ResourcesAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Resources', repository_interface=IResourcesRepository)
__all__ = ['ResourcesAdapter']