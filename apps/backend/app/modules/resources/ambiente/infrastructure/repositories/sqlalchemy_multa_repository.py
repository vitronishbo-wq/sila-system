from __future__ import annotations
from datetime import date
from app.modules.resources.ambiente.application.ports.multa_repository_port import MultaRepositoryPort
from app.modules.resources.ambiente.domain.enums import StatusMulta
from app.modules.resources.ambiente.domain.models.multa import Multa

class SQLAlchemyMultaRepository(MultaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, Multa] = {}
        self._seq = 0

    async def save(self, item: Multa) -> Multa:
        self._items[item.numero_multa] = item
        return item

    async def get_by_numero(self, numero_multa: str) -> Multa | None:
        return self._items.get(numero_multa)

    async def list(self, *, numero_auto_infracao: str | None=None, status: StatusMulta | None=None) -> list[Multa]:
        values = list(self._items.values())
        if numero_auto_infracao:
            values = [item for item in values if item.numero_auto_infracao == numero_auto_infracao]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f'MULT/{date.today().year}/{self._seq:06d}'