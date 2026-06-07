from __future__ import annotations

import builtins
from typing import Protocol
from uuid import UUID

from ...domain.entities.taxpayer import Taxpayer


class TaxpayerRepositoryPort(Protocol):
    async def add(self, entity: Taxpayer) -> Taxpayer: ...

    async def get(self, id: UUID) -> Taxpayer | None: ...

    async def get_by_nif(self, nif: str) -> Taxpayer | None: ...

    async def list(self, limit: int = 100, offset: int = 0) -> builtins.list[Taxpayer]: ...

    async def update(self, entity: Taxpayer) -> Taxpayer: ...

    async def delete(self, id: UUID) -> None: ...
