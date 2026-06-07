"""Infrastructure adapters for Educacao module"""

from apps.backend.app.modules.educacao.domain.repositories import IEducacaoRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

EducacaoAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Educacao", repository_interface=IEducacaoRepository
)
__all__ = ["EducacaoAdapter"]
