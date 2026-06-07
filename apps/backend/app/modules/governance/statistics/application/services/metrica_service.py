from __future__ import annotations

from apps.backend.app.modules.governance.statistics.application.ports.metrica_repository_port import (
    MetricaRepositoryPort,
)
from apps.backend.app.modules.governance.statistics.domain.enums import FonteDados, TipoMetrica
from apps.backend.app.modules.governance.statistics.domain.models.metrica import Metrica
from apps.backend.app.modules.governance.statistics.exceptions import (
    EstatisticaConflictError,
    EstatisticaNotFoundError,
)


class MetricaService:
    def __init__(self, metrica_repository: MetricaRepositoryPort) -> None:
        self.metrica_repository = metrica_repository

    async def criar_metrica(self, data: dict) -> Metrica:
        if await self.metrica_repository.get_by_nome(data["nome"]):
            raise EstatisticaConflictError("Metrica com este nome ja existe")
        metrica = Metrica(**data)
        return await self.metrica_repository.create(metrica)

    async def listar_metricas(
        self,
        tipo: TipoMetrica | None = None,
        fonte: FonteDados | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Metrica]:
        if tipo is not None:
            return await self.metrica_repository.list_by_tipo(tipo=tipo, limit=limit)
        if fonte is not None:
            return await self.metrica_repository.list_by_fonte(fonte=fonte, limit=limit)
        return await self.metrica_repository.list_all(limit=limit, offset=offset)

    async def obter_metrica(self, metrica_id: int) -> Metrica:
        metrica = await self.metrica_repository.get_by_id(metrica_id)
        if not metrica:
            raise EstatisticaNotFoundError("Metrica nao encontrada")
        return metrica

    async def atualizar_metrica(self, metrica_id: int, data: dict) -> Metrica:
        metrica = await self.obter_metrica(metrica_id)
        for key, value in data.items():
            if value is not None and hasattr(metrica, key):
                setattr(metrica, key, value)
        return await self.metrica_repository.update(metrica)

    async def atualizar_valor(self, metrica_id: int, valor: float) -> Metrica:
        metrica = await self.obter_metrica(metrica_id)
        metrica.atualizar_valor(valor)
        return await self.metrica_repository.update(metrica)

    async def deletar_metrica(self, metrica_id: int) -> None:
        deleted = await self.metrica_repository.delete(metrica_id)
        if not deleted:
            raise EstatisticaNotFoundError("Metrica nao encontrada")
