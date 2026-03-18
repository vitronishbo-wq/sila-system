from abc import ABC, abstractmethod
from typing import List, Optional
from apps.backend.app.modules.procurement.domain.models.tender import Tender

class TenderRepositoryPort(ABC):
    """Port: Tender persistence interface."""

    @abstractmethod
    async def create(self, tender: Tender) -> Tender:
        pass

    @abstractmethod
    async def save(self, tender: Tender) -> Tender:
        pass

    @abstractmethod
    async def get_by_id(self, tender_id: str) -> Optional[Tender]:
        pass

    @abstractmethod
    async def list_by_status(self, status: str, limit: int=100, offset: int=0) -> List[Tender]:
        pass

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> List[Tender]:
        pass

    @abstractmethod
    async def delete(self, tender_id: str) -> bool:
        pass