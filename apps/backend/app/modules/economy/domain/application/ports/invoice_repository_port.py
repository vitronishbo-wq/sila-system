from abc import ABC, abstractmethod
from typing import List, Optional
from apps.backend.app.modules.economy.domain.models.invoice import Invoice

class InvoiceRepositoryPort(ABC):
    """ Contrato de repositório para Invoice. """

    @abstractmethod
    async def create(self, invoice: Invoice) -> Invoice:
        pass

    @abstractmethod
    async def save(self, invoice: Invoice) -> Invoice:
        pass

    @abstractmethod
    async def get_by_id(self, invoice_id: str) -> Optional[Invoice]:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: str) -> List[Invoice]:
        pass

    @abstractmethod
    async def get_pending(self, citizen_id: str) -> List[Invoice]:
        pass

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> List[Invoice]:
        pass

    @abstractmethod
    async def delete(self, invoice_id: str) -> bool:
        pass
