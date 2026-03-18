from abc import ABC, abstractmethod
from typing import List, Optional
from apps.backend.app.modules.procurement.domain.models.bid import Bid

class BidRepositoryPort(ABC):
    """Port: Bid persistence interface."""

    @abstractmethod
    async def create(self, bid: Bid) -> Bid:
        pass

    @abstractmethod
    async def save(self, bid: Bid) -> Bid:
        pass

    @abstractmethod
    async def get_by_id(self, bid_id: str) -> Optional[Bid]:
        pass

    @abstractmethod
    async def list_by_tender(self, tender_id: str, limit: int=100, offset: int=0) -> List[Bid]:
        pass

    @abstractmethod
    async def list_by_supplier(self, supplier_id: str, limit: int=100, offset: int=0) -> List[Bid]:
        pass

    @abstractmethod
    async def list_by_status(self, status: str, limit: int=100, offset: int=0) -> List[Bid]:
        pass

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> List[Bid]:
        pass

    @abstractmethod
    async def delete(self, bid_id: str) -> bool:
        pass