from __future__ import annotations
from datetime import datetime
from uuid import UUID
from app.modules.infrastructure_sector.aviacao_civil.application.ports.ocorrencia_repository_port import OcorrenciaRepositoryPort
from app.modules.infrastructure_sector.aviacao_civil.domain.models.ocorrencia import Ocorrencia

class InMemoryOcorrenciaRepository(OcorrenciaRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Ocorrencia] = {}

    async def save(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        self._items[ocorrencia.id] = ocorrencia
        return ocorrencia

    async def get_by_id(self, ocorrencia_id: UUID) -> Ocorrencia | None:
        return self._items.get(ocorrencia_id)

    async def list_all(self) -> list[Ocorrencia]:
        return sorted(self._items.values(), key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[Ocorrencia]:
        return [item for item in self._items.values() if inicio <= item.data_ocorrencia <= fim]