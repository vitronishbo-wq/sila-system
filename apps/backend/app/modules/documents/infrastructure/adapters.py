"""Infrastructure adapters for Documents module"""

from apps.backend.app.modules.documents.domain.repositories import IDocumentsRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

DocumentsAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Documents", repository_interface=IDocumentsRepository
)
__all__ = ["DocumentsAdapter"]
