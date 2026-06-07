from abc import ABC, abstractmethod

from apps.backend.app.modules.procurement.domain.models.supplier import Supplier


class SupplierRepositoryPort(ABC):
    """Port: Supplier persistence interface."""

    @abstractmethod
    async def create(self, supplier: Supplier) -> Supplier:
        pass

    @abstractmethod
    async def save(self, supplier: Supplier) -> Supplier:
        pass

    @abstractmethod
    async def get_by_id(self, supplier_id: str) -> Supplier | None:
        pass

    @abstractmethod
    async def get_by_tax_id(self, tax_id: str) -> Supplier | None:
        pass

    @abstractmethod
    async def list_by_status(
        self, status: str, limit: int = 100, offset: int = 0
    ) -> list[Supplier]:
        pass

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Supplier]:
        pass

    @abstractmethod
    async def delete(self, supplier_id: str) -> bool:
        pass
