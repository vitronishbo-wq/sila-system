"""Infrastructure adapters for Educacao module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.educacao.domain.repositories import IEducacaoRepository
EducacaoAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Educacao', repository_interface=IEducacaoRepository)
__all__ = ['EducacaoAdapter']