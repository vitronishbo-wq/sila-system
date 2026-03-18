"""Infrastructure adapters for Tourism module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.tourism.domain.repositories import ITourismRepository
TourismAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Tourism', repository_interface=ITourismRepository)
__all__ = ['TourismAdapter']