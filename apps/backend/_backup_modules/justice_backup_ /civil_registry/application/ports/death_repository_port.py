from abc import ABC, abstractmethod
from typing import Optional
from apps.backend.app.modules.justice.bounded_contexts.infrastructure.models.death_record import DeathRecord

class DeathRepositoryPort(ABC):
    """Porta (Interface) para o Repositório de Óbitos."""

    @abstractmethod
    async def save(self, death: DeathRecord) -> DeathRecord:
        pass

    @abstractmethod
    async def get_by_id(self, death_id: str) -> Optional[DeathRecord]:
        pass

    @abstractmethod
    async def get_by_citizen_id(self, citizen_id: str) -> Optional[DeathRecord]:
        pass