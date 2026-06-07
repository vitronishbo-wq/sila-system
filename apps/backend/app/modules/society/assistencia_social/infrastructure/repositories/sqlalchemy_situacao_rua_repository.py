from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.assistencia_social.application.ports.situacao_rua_repository_port import (
    SituacaoRuaRepositoryPort,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento
from apps.backend.app.modules.society.assistencia_social.domain.models import SituacaoRua
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.situacao_rua_model import (
    SituacaoRuaModel,
)


class SQLAlchemySituacaoRuaRepository(SituacaoRuaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: SituacaoRua) -> SituacaoRua:
        model = await self.session.get(SituacaoRuaModel, entity.id)
        if model is None:
            model = SituacaoRuaModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.beneficiario_id = entity.beneficiario_id
        model.data_registro = entity.data_registro
        model.localizacao = entity.localizacao
        model.motivo = entity.motivo
        model.status = entity.status.value
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> SituacaoRua | None:
        model = await self.session.get(SituacaoRuaModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[SituacaoRua]:
        stmt = (
            select(SituacaoRuaModel)
            .where(SituacaoRuaModel.beneficiario_id == beneficiario_id)
            .order_by(SituacaoRuaModel.data_registro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[SituacaoRua]:
        stmt = select(SituacaoRuaModel).order_by(SituacaoRuaModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(SituacaoRuaModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: SituacaoRuaModel) -> SituacaoRua:
        return SituacaoRua(
            id=model.id,
            codigo=model.codigo,
            beneficiario_id=model.beneficiario_id,
            data_registro=model.data_registro,
            localizacao=model.localizacao,
            motivo=model.motivo,
            status=StatusAcompanhamento(model.status),
        )
