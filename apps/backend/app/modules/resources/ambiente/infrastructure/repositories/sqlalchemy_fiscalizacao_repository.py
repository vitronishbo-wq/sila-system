from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.ambiente.application.ports.fiscalizacao_repository_port import (
    FiscalizacaoRepositoryPort,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusFiscalizacao
from apps.backend.app.modules.resources.ambiente.domain.models.fiscalizacao import Fiscalizacao


class SQLAlchemyFiscalizacaoRepository(FiscalizacaoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, Fiscalizacao] = {}
        self._seq = 0

    async def save(self, item: Fiscalizacao) -> Fiscalizacao:
        self._items[item.numero_fiscalizacao] = item
        return item

    async def get_by_numero(self, numero_fiscalizacao: str) -> Fiscalizacao | None:
        return self._items.get(numero_fiscalizacao)

    async def list(
        self, *, numero_licenca: str | None = None, status: StatusFiscalizacao | None = None
    ) -> list[Fiscalizacao]:
        values = list(self._items.values())
        if numero_licenca:
            values = [item for item in values if item.numero_licenca == numero_licenca]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f"FIS/{date.today().year}/{self._seq:06d}"
