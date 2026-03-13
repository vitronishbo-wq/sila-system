from __future__ import annotations
from datetime import date
from app.modules.resources.ambiente.application.ports.embargo_repository_port import EmbargoRepositoryPort
from app.modules.resources.ambiente.domain.enums import StatusEmbargo
from app.modules.resources.ambiente.domain.models.embargo import Embargo

class SQLAlchemyEmbargoRepository(EmbargoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, Embargo] = {}
        self._seq = 0

    async def save(self, item: Embargo) -> Embargo:
        self._items[item.numero_embargo] = item
        return item

    async def get_by_numero(self, numero_embargo: str) -> Embargo | None:
        return self._items.get(numero_embargo)

    async def list(self, *, numero_auto_infracao: str | None=None, status: StatusEmbargo | None=None) -> list[Embargo]:
        values = list(self._items.values())
        if numero_auto_infracao:
            values = [item for item in values if item.numero_auto_infracao == numero_auto_infracao]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f'EMB/{date.today().year}/{self._seq:06d}'