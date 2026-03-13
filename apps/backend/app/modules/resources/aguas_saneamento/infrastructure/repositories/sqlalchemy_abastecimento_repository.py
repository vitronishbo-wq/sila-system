from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.abastecimento_repository_port import AbastecimentoRepositoryPort
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.abastecimento import AbastecimentoAgua

class SQLAlchemyAbastecimentoRepository(AbastecimentoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, AbastecimentoAgua] = {}
        self._seq = 0

    async def save(self, item: AbastecimentoAgua) -> AbastecimentoAgua:
        self._items[item.codigo_abastecimento] = item
        return item

    async def get_by_codigo(self, codigo_abastecimento: str) -> AbastecimentoAgua | None:
        return self._items.get(codigo_abastecimento)

    async def list(self, *, infraestrutura_id: UUID | None=None, status: StatusAbastecimento | None=None, provincia: str | None=None, municipio: str | None=None) -> list[AbastecimentoAgua]:
        values = list(self._items.values())
        if infraestrutura_id:
            values = [item for item in values if item.infraestrutura_id == infraestrutura_id]
        if status:
            values = [item for item in values if item.status == status]
        if provincia:
            prov = provincia.strip().lower()
            values = [item for item in values if item.provincia.lower() == prov]
        if municipio:
            mun = municipio.strip().lower()
            values = [item for item in values if item.municipio.lower() == mun]
        return values

    async def next_codigo(self) -> str:
        self._seq += 1
        return f'ABS/{date.today().year}/{self._seq:06d}'