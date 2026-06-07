from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.society.juventude.application.ports.politica_juventude_repository_port import (
    PoliticaJuventudeRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusPoliticaJuventude,
)
from apps.backend.app.modules.society.juventude.domain.models.politica_juventude import (
    PoliticaJuventude,
)


class PoliticaJuventudeService:
    def __init__(self, *, politica_repo: PoliticaJuventudeRepositoryPort) -> None:
        self.politica_repo = politica_repo

    async def criar_politica(
        self,
        *,
        nome: str,
        descricao: str,
        area_interesse: AreaInteresse,
        data_inicio: date,
        metas: dict[str, float] | None = None,
        indicadores: list[str] | None = None,
        data_fim: date | None = None,
        observacoes: str | None = None,
    ) -> PoliticaJuventude:
        codigo = await self.politica_repo.next_codigo()
        item = PoliticaJuventude.criar(
            codigo_politica=codigo,
            nome=nome,
            descricao=descricao,
            area_interesse=area_interesse,
            data_inicio=data_inicio,
            metas=metas,
            indicadores=indicadores,
            data_fim=data_fim,
            observacoes=observacoes,
        )
        return await self.politica_repo.save(item)

    async def buscar_politica(self, politica_id: UUID) -> PoliticaJuventude:
        item = await self.politica_repo.get_by_id(politica_id)
        if item is None:
            raise ValueError("Politica de juventude nao encontrada")
        return item

    async def listar_politicas(
        self, *, status: StatusPoliticaJuventude | None = None, area: AreaInteresse | None = None
    ) -> list[PoliticaJuventude]:
        if status is not None:
            return await self.politica_repo.list_by_status(status)
        if area is not None:
            return await self.politica_repo.list_by_area(area)
        return await self.politica_repo.list_all()

    async def atualizar_status(
        self, *, politica_id: UUID, status: StatusPoliticaJuventude
    ) -> PoliticaJuventude:
        item = await self.buscar_politica(politica_id)
        item.atualizar_status(status)
        return await self.politica_repo.save(item)

    async def remover_politica(self, politica_id: UUID) -> None:
        if not await self.politica_repo.delete(politica_id):
            raise ValueError("Politica de juventude nao encontrada")
