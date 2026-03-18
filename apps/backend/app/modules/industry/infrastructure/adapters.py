"""Infrastructure adapters for Industry module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.industry.domain.repositories import IIndustryRepository
IndustryAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Industry', repository_interface=IIndustryRepository)
__all__ = ['IndustryAdapter']