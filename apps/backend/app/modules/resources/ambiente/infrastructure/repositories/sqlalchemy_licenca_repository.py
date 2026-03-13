from __future__ import annotations
from datetime import date
from apps.backend.app.modules.resources.ambiente.application.ports.licenca_repository_port import LicencaRepositoryPort
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusLicenca, TipoLicenca
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_ambiental import LicencaAmbiental

class SQLAlchemyLicencaRepository(LicencaRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[str, LicencaAmbiental] = {}
        self._seq = 0

    async def save(self, item: LicencaAmbiental) -> LicencaAmbiental:
        self._items[item.numero_licenca] = item
        return item

    async def get_by_numero(self, numero_licenca: str) -> LicencaAmbiental | None:
        return self._items.get(numero_licenca)

    async def list(self, *, numero_car: str | None=None, tipo: TipoLicenca | None=None, status: StatusLicenca | None=None) -> list[LicencaAmbiental]:
        values = list(self._items.values())
        if numero_car:
            values = [item for item in values if item.numero_car == numero_car]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f'LIC/{date.today().year}/{self._seq:06d}'