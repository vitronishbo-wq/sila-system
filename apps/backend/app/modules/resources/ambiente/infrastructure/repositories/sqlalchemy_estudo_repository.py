from __future__ import annotations
from datetime import date
from apps.backend.app.modules.resources.ambiente.application.ports.estudo_repository_port import EstudoRepositoryPort
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusEstudoAmbiental, TipoEstudoAmbiental
from apps.backend.app.modules.resources.ambiente.domain.models.estudo_impacto import EstudoImpacto

class SQLAlchemyEstudoRepository(EstudoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, EstudoImpacto] = {}
        self._seq = 0

    async def save(self, item: EstudoImpacto) -> EstudoImpacto:
        self._items[item.numero_estudo] = item
        return item

    async def get_by_numero(self, numero_estudo: str) -> EstudoImpacto | None:
        return self._items.get(numero_estudo)

    async def list(self, *, numero_licenca: str | None=None, tipo: TipoEstudoAmbiental | None=None, status: StatusEstudoAmbiental | None=None) -> list[EstudoImpacto]:
        values = list(self._items.values())
        if numero_licenca:
            values = [item for item in values if item.numero_licenca == numero_licenca]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f'EST/{date.today().year}/{self._seq:06d}'