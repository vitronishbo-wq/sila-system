from abc import ABC, abstractmethod
from typing import Optional, List
from app.modules.justice.bounded_contexts.infrastructure.models.birth_record import BirthRecord

class BirthRepositoryPort(ABC):
    """Porta (Interface) para o Repositório de Nascimentos."""

    @abstractmethod
    async def save(self, birth: BirthRecord) -> BirthRecord:
        pass

    @abstractmethod
    async def get_by_id(self, birth_id: str) -> Optional[BirthRecord]:
        pass

    @abstractmethod
    async def get_by_nub(self, nub: str) -> Optional[BirthRecord]:
        pass

    @abstractmethod
    async def list_all(self, limit: int=10, offset: int=0) -> List[BirthRecord]:
        pass