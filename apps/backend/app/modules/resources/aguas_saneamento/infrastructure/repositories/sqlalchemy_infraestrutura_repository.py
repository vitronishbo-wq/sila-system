from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.aguas_saneamento.application.ports.infraestrutura_repository_port import (
    InfraestruturaRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    StatusInfraestrutura,
    TipoInfraestrutura,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.infraestrutura import (
    InfraestruturaHidrica,
)


class SQLAlchemyInfraestruturaRepository(InfraestruturaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, InfraestruturaHidrica] = {}
        self._seq = 0

    async def save(self, item: InfraestruturaHidrica) -> InfraestruturaHidrica:
        self._items[item.codigo_infraestrutura] = item
        return item

    async def get_by_codigo(self, codigo_infraestrutura: str) -> InfraestruturaHidrica | None:
        return self._items.get(codigo_infraestrutura)

    async def list(
        self,
        *,
        tipo: TipoInfraestrutura | None = None,
        status: StatusInfraestrutura | None = None,
        provincia: str | None = None,
        municipio: str | None = None,
    ) -> list[InfraestruturaHidrica]:
        values = list(self._items.values())
        if tipo:
            values = [item for item in values if item.tipo == tipo]
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
        return f"INF/{date.today().year}/{self._seq:06d}"
