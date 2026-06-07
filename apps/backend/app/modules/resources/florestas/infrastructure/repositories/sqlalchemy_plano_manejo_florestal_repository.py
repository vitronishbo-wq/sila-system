from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.resources.florestas.application.ports.plano_manejo_florestal_repository_port import (
    PlanoManejoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.domain.enums import StatusPlanoManejo
from apps.backend.app.modules.resources.florestas.domain.models.plano_manejo_florestal import (
    PlanoManejoFlorestal,
)
from apps.backend.app.modules.resources.florestas.infrastructure.models.plano_manejo_florestal_model import (
    PlanoManejoFlorestalModel,
)


class SQLAlchemyPlanoManejoFlorestalRepository(PlanoManejoFlorestalRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, plano: PlanoManejoFlorestal) -> PlanoManejoFlorestal:
        model = await self.session.get(PlanoManejoFlorestalModel, plano.id)
        if not model:
            model = PlanoManejoFlorestalModel(id=plano.id)
            self.session.add(model)
        model.numero_pmfs = plano.numero_pmfs
        model.unidade_manejo_id = plano.unidade_manejo_id
        model.responsavel_tecnico_id = plano.responsavel_tecnico_id
        model.responsavel_tecnico_registro = plano.responsavel_tecnico_registro
        model.status = plano.status.value
        model.data_submissao = plano.data_submissao
        model.data_aprovacao = plano.data_aprovacao
        model.data_validade = plano.data_validade
        model.analista_responsavel_id = plano.analista_responsavel_id
        model.volume_anual_estimado_m3 = plano.volume_anual_estimado_m3
        model.ciclo_corte_anos = plano.ciclo_corte_anos
        model.area_anual_ha = plano.area_anual_ha
        model.parecer_tecnico = plano.parecer_tecnico
        model.observacoes = plano.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, plano_id: UUID) -> PlanoManejoFlorestal | None:
        model = await self.session.get(PlanoManejoFlorestalModel, plano_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_pmfs: str) -> PlanoManejoFlorestal | None:
        stmt = select(PlanoManejoFlorestalModel).where(
            PlanoManejoFlorestalModel.numero_pmfs == numero_pmfs
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_unidade(self, unidade_manejo_id: UUID) -> list[PlanoManejoFlorestal]:
        stmt = select(PlanoManejoFlorestalModel).where(
            PlanoManejoFlorestalModel.unidade_manejo_id == unidade_manejo_id
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(model: PlanoManejoFlorestalModel) -> PlanoManejoFlorestal:
        return PlanoManejoFlorestal(
            id=model.id,
            numero_pmfs=model.numero_pmfs,
            unidade_manejo_id=model.unidade_manejo_id,
            responsavel_tecnico_id=model.responsavel_tecnico_id,
            responsavel_tecnico_registro=model.responsavel_tecnico_registro,
            status=StatusPlanoManejo(model.status),
            data_submissao=model.data_submissao,
            data_aprovacao=model.data_aprovacao,
            data_validade=model.data_validade,
            analista_responsavel_id=model.analista_responsavel_id,
            volume_anual_estimado_m3=model.volume_anual_estimado_m3,
            ciclo_corte_anos=model.ciclo_corte_anos,
            area_anual_ha=model.area_anual_ha,
            parecer_tecnico=model.parecer_tecnico,
            observacoes=model.observacoes,
        )


SqlalchemyPlanoManejoFlorestalRepository = SQLAlchemyPlanoManejoFlorestalRepository
