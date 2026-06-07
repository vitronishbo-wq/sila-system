from __future__ import annotations

from apps.backend.app.modules.governance.statistics.application.bus import EventBus
from apps.backend.app.modules.governance.statistics.application.ports.kpi_repository_port import (
    KPIRepositoryPort,
)
from apps.backend.app.modules.governance.statistics.application.ports.metrica_repository_port import (
    MetricaRepositoryPort,
)
from apps.backend.app.modules.governance.statistics.domain.enums import StatusKPI
from apps.backend.app.modules.governance.statistics.domain.models.kpi import KPI
from apps.backend.app.modules.governance.statistics.exceptions import (
    EstatisticaConflictError,
    EstatisticaNotFoundError,
)


class KPIService:
    def __init__(
        self,
        kpi_repository: KPIRepositoryPort,
        metrica_repository: MetricaRepositoryPort,
        event_bus: EventBus | None = None,
    ) -> None:
        self.kpi_repository = kpi_repository
        self.metrica_repository = metrica_repository
        self.event_bus = event_bus

    async def criar_kpi(self, data: dict) -> KPI:
        if await self.kpi_repository.get_by_nome(data["nome"]):
            raise EstatisticaConflictError("KPI com este nome ja existe")
        if not await self.metrica_repository.get_by_id(data["metrica_id"]):
            raise EstatisticaNotFoundError("Metrica referenciada nao existe")
        kpi = KPI(**data)
        saved = await self.kpi_repository.create(kpi)
        if self.event_bus:
            self.event_bus.publish(
                "kpi.criado", {"id": saved.id, "nome": saved.nome, "metrica_id": saved.metrica_id}
            )
        return saved

    async def atualizar_kpi(self, kpi_id: int, data: dict) -> KPI:
        kpi = await self.kpi_repository.get_by_id(kpi_id)
        if not kpi:
            raise EstatisticaNotFoundError("KPI nao encontrado")
        for key, value in data.items():
            if value is not None and hasattr(kpi, key):
                setattr(kpi, key, value)
        updated = await self.kpi_repository.update(kpi)
        if self.event_bus:
            self.event_bus.publish(
                "kpi.atualizado",
                {
                    "id": updated.id,
                    "valor_atual": updated.valor_atual,
                    "performance": updated.calcular_performance(),
                },
            )
        return updated

    async def atualizar_valor_kpi(self, kpi_id: int, valor: float) -> KPI:
        kpi = await self.kpi_repository.get_by_id(kpi_id)
        if not kpi:
            raise EstatisticaNotFoundError("KPI nao encontrado")
        valor_anterior = kpi.valor_atual
        kpi.atualizar_valor(valor)
        updated = await self.kpi_repository.update(kpi)
        if self.event_bus:
            self.event_bus.publish(
                "kpi.valor_atualizado",
                {
                    "id": updated.id,
                    "valor_anterior": valor_anterior,
                    "valor_atual": valor,
                    "performance": updated.calcular_performance(),
                },
            )
        return updated

    async def listar_kpis(
        self, status: StatusKPI | None = None, limit: int = 100, offset: int = 0
    ) -> list[KPI]:
        if status:
            return await self.kpi_repository.list_by_status(status=status, limit=limit)
        return await self.kpi_repository.list_all(limit=limit, offset=offset)

    async def obter_kpi(self, kpi_id: int) -> KPI:
        kpi = await self.kpi_repository.get_by_id(kpi_id)
        if not kpi:
            raise EstatisticaNotFoundError("KPI nao encontrado")
        return kpi

    async def calcular_performance_kpi(self, kpi_id: int) -> dict:
        kpi = await self.obter_kpi(kpi_id)
        return {
            "kpi_id": kpi.id,
            "nome": kpi.nome,
            "valor_atual": kpi.valor_atual,
            "valor_alvo": kpi.valor_alvo,
            "performance": kpi.calcular_performance(),
            "status_cor": kpi.status_cor,
            "dentro_limites": kpi.esta_within_limits(),
        }

    async def get_kpis_criticos(self, limit: int = 50) -> list[KPI]:
        ativos = await self.kpi_repository.list_by_status(StatusKPI.ATIVO, limit=10000)
        criticos = [k for k in ativos if k.status_cor == "vermelho"]
        return criticos[:limit]

    async def deletar_kpi(self, kpi_id: int) -> None:
        if not await self.kpi_repository.delete(kpi_id):
            raise EstatisticaNotFoundError("KPI nao encontrado")
