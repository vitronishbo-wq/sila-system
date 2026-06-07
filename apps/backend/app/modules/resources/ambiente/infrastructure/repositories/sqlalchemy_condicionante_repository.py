from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.ambiente.application.ports.condicionante_repository_port import (
    CondicionanteRepositoryPort,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCondicionante
from apps.backend.app.modules.resources.ambiente.domain.models.condicionante import Condicionante


class SQLAlchemyCondicionanteRepository(CondicionanteRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, Condicionante] = {}
        self._seq = 0

    async def save(self, item: Condicionante) -> Condicionante:
        self._items[item.codigo_condicionante] = item
        return item

    async def get_by_codigo(self, codigo_condicionante: str) -> Condicionante | None:
        return self._items.get(codigo_condicionante)

    async def list(
        self, *, numero_licenca: str | None = None, status: StatusCondicionante | None = None
    ) -> list[Condicionante]:
        values = list(self._items.values())
        if numero_licenca:
            values = [item for item in values if item.numero_licenca == numero_licenca]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_codigo(self) -> str:
        self._seq += 1
        return f"COND/{date.today().year}/{self._seq:06d}"
