from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.resources.aguas_saneamento.application.ports.fatura_repository_port import (
    FaturaRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusFatura
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.fatura_agua import FaturaAgua


class SQLAlchemyFaturaRepository(FaturaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, FaturaAgua] = {}
        self._seq = 0

    async def save(self, item: FaturaAgua) -> FaturaAgua:
        self._items[item.numero_fatura] = item
        return item

    async def get_by_numero(self, numero_fatura: str) -> FaturaAgua | None:
        return self._items.get(numero_fatura)

    async def list(
        self,
        *,
        consumo_id: UUID | None = None,
        titular_id: UUID | None = None,
        referencia: str | None = None,
        status: StatusFatura | None = None,
    ) -> list[FaturaAgua]:
        values = list(self._items.values())
        if consumo_id:
            values = [item for item in values if item.consumo_id == consumo_id]
        if titular_id:
            values = [item for item in values if item.titular_id == titular_id]
        if referencia:
            values = [item for item in values if item.referencia == referencia]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f"FAT/{date.today().year}/{self._seq:06d}"
