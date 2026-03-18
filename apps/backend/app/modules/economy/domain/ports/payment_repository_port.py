from abc import ABC, abstractmethod
from typing import List, Optional
from apps.backend.app.modules.economy.domain.models.payment import Payment

class PaymentRepositoryPort(ABC):
    """ Contrato de repositório para Payment. """

    @abstractmethod
    async def create(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: str) -> List[Payment]:
        pass

    @abstractmethod
    async def list_by_invoice(self, invoice_id: str) -> List[Payment]:
        pass

    @abstractmethod
    async def get_by_gateway_ref(self, gateway_reference: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def exists_by_gateway_ref(self, gateway_reference: str) -> bool:
        pass

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> List[Payment]:
        pass

    @abstractmethod
    async def delete(self, payment_id: str) -> bool:
        pass