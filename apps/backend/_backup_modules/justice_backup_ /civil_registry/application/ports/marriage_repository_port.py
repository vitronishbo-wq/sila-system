from abc import ABC, abstractmethod
from typing import Optional, List
from app.modules.justice.bounded_contexts.infrastructure.models.marriage_record import MarriageRecord

class MarriageRepositoryPort(ABC):
    """Porta (Interface) para o Repositório de Casamentos."""

    @abstractmethod
    async def save(self, marriage: MarriageRecord) -> MarriageRecord:
        pass

    @abstractmethod
    async def get_by_id(self, marriage_id: str) -> Optional[MarriageRecord]:
        pass

    @abstractmethod
    async def list_by_spouse(self, citizen_id: str) -> List[MarriageRecord]:
        pass