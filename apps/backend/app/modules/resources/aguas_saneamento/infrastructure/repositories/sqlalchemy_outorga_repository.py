from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.aguas_saneamento.application.ports.outorga_repository_port import OutorgaRepositoryPort
from app.modules.resources.aguas_saneamento.domain.enums import StatusOutorga, TipoOutorga
from app.modules.resources.aguas_saneamento.domain.models.outorga import Outorga

class SQLAlchemyOutorgaRepository(OutorgaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, Outorga] = {}
        self._seq = 0

    async def save(self, item: Outorga) -> Outorga:
        self._items[item.numero_outorga] = item
        return item

    async def get_by_numero(self, numero_outorga: str) -> Outorga | None:
        return self._items.get(numero_outorga)

    async def list(self, *, requerente_id: UUID | None=None, tipo: TipoOutorga | None=None, status: StatusOutorga | None=None) -> list[Outorga]:
        values = list(self._items.values())
        if requerente_id:
            values = [item for item in values if item.requerente_id == requerente_id]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f'OUT/{date.today().year}/{self._seq:06d}'