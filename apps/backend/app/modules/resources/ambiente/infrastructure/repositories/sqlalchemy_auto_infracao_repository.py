from __future__ import annotations
from datetime import date
from app.modules.resources.ambiente.application.ports.auto_infracao_repository_port import AutoInfracaoRepositoryPort
from app.modules.resources.ambiente.domain.enums import StatusAutoInfracao, TipoAutoInfracao
from app.modules.resources.ambiente.domain.models.auto_infracao import AutoInfracao

class SQLAlchemyAutoInfracaoRepository(AutoInfracaoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, AutoInfracao] = {}
        self._seq = 0

    async def save(self, item: AutoInfracao) -> AutoInfracao:
        self._items[item.numero_auto] = item
        return item

    async def get_by_numero(self, numero_auto: str) -> AutoInfracao | None:
        return self._items.get(numero_auto)

    async def list(self, *, numero_fiscalizacao: str | None=None, tipo: TipoAutoInfracao | None=None, status: StatusAutoInfracao | None=None) -> list[AutoInfracao]:
        values = list(self._items.values())
        if numero_fiscalizacao:
            values = [item for item in values if item.numero_fiscalizacao == numero_fiscalizacao]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f'AINF/{date.today().year}/{self._seq:06d}'