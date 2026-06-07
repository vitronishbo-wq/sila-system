from abc import ABC, abstractmethod

from apps.backend.app.modules.procurement.domain.models.contract import Contract


class ContractRepositoryPort(ABC):
    """Port: Contract persistence interface."""

    @abstractmethod
    async def create(self, contract: Contract) -> Contract:
        pass

    @abstractmethod
    async def save(self, contract: Contract) -> Contract:
        pass

    @abstractmethod
    async def get_by_id(self, contract_id: str) -> Contract | None:
        pass

    @abstractmethod
    async def list_by_status(
        self, status: str, limit: int = 100, offset: int = 0
    ) -> list[Contract]:
        pass

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Contract]:
        pass

    @abstractmethod
    async def delete(self, contract_id: str) -> bool:
        pass
