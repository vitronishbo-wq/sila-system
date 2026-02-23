from __future__ import annotations
from typing import Protocol, List, Optional
from uuid import UUID

from ...domain.entities.taxpayer import Taxpayer


class TaxpayerRepositoryPort(Protocol):
    async def add(self, entity: Taxpayer) -> Taxpayer:
        ...

    async def get(self, id: UUID) -> Optional[Taxpayer]:
        ...

    async def get_by_nif(self, nif: str) -> Optional[Taxpayer]:
        ...

    async def list(self, limit: int = 100, offset: int = 0) -> List[Taxpayer]:
        ...

    async def update(self, entity: Taxpayer) -> Taxpayer:
        ...

    async def delete(self, id: UUID) -> None:
        ...
