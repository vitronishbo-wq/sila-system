from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.assistencia_social.application.ports.visita_domiciliar_repository_port import (
    VisitaDomiciliarRepositoryPort,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import ResultadoVisita
from apps.backend.app.modules.society.assistencia_social.domain.models import VisitaDomiciliar
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.visita_domiciliar_model import (
    VisitaDomiciliarModel,
)


class SQLAlchemyVisitaDomiciliarRepository(VisitaDomiciliarRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: VisitaDomiciliar) -> VisitaDomiciliar:
        model = await self.session.get(VisitaDomiciliarModel, entity.id)
        if model is None:
            model = VisitaDomiciliarModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.beneficiario_id = entity.beneficiario_id
        model.assistente_social_id = entity.assistente_social_id
        model.data_visita = entity.data_visita
        model.condicoes_moradia = entity.condicoes_moradia
        model.observacoes = entity.observacoes
        model.recomendacoes = entity.recomendacoes
        model.resultado = entity.resultado.value
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> VisitaDomiciliar | None:
        model = await self.session.get(VisitaDomiciliarModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[VisitaDomiciliar]:
        stmt = (
            select(VisitaDomiciliarModel)
            .where(VisitaDomiciliarModel.beneficiario_id == beneficiario_id)
            .order_by(VisitaDomiciliarModel.data_visita.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[VisitaDomiciliar]:
        stmt = select(VisitaDomiciliarModel).order_by(VisitaDomiciliarModel.data_visita.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(VisitaDomiciliarModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: VisitaDomiciliarModel) -> VisitaDomiciliar:
        return VisitaDomiciliar(
            id=model.id,
            codigo=model.codigo,
            beneficiario_id=model.beneficiario_id,
            assistente_social_id=model.assistente_social_id,
            data_visita=model.data_visita,
            condicoes_moradia=model.condicoes_moradia,
            observacoes=model.observacoes,
            recomendacoes=model.recomendacoes or [],
            resultado=ResultadoVisita(model.resultado),
        )
