from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.aguas_saneamento.application.ports.consumo_repository_port import ConsumoRepositoryPort
from app.modules.resources.aguas_saneamento.domain.enums import StatusConsumo
from app.modules.resources.aguas_saneamento.domain.models.consumo_agua import ConsumoAgua

class SQLAlchemyConsumoRepository(ConsumoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, ConsumoAgua] = {}
        self._seq = 0

    async def save(self, item: ConsumoAgua) -> ConsumoAgua:
        self._items[item.codigo_consumo] = item
        return item

    async def get_by_codigo(self, codigo_consumo: str) -> ConsumoAgua | None:
        return self._items.get(codigo_consumo)

    async def list(self, *, abastecimento_id: UUID | None=None, titular_id: UUID | None=None, referencia: str | None=None, status: StatusConsumo | None=None) -> list[ConsumoAgua]:
        values = list(self._items.values())
        if abastecimento_id:
            values = [item for item in values if item.abastecimento_id == abastecimento_id]
        if titular_id:
            values = [item for item in values if item.titular_id == titular_id]
        if referencia:
            values = [item for item in values if item.referencia == referencia]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_codigo(self) -> str:
        self._seq += 1
        return f'CON/{date.today().year}/{self._seq:06d}'