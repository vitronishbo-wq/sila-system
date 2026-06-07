from typing import Any


class CivilRegistryAdapter:
    """Compatibility adapter for justice.civil_registry imports."""

    def __init__(self, repository: Any = None):
        self.repository = repository

    def list_documents(self, citizen_id: str) -> list[Any]:
        if self.repository and hasattr(self.repository, "list_by_citizen"):
            return self.repository.list_by_citizen(citizen_id)
        return []

    def get_document(self, document_id: str) -> Any | None:
        if self.repository and hasattr(self.repository, "get_by_id"):
            return self.repository.get_by_id(document_id)
        return None
