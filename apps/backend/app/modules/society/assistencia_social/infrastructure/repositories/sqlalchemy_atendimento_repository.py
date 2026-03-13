from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.assistencia_social.application.ports.atendimento_repository_port import AtendimentoRepositoryPort
from app.modules.society.assistencia_social.domain.enums import StatusAcompanhamento, TipoAtendimento
from app.modules.society.assistencia_social.domain.models import Atendimento
from app.modules.society.assistencia_social.infrastructure.models.atendimento_model import AtendimentoModel

class SQLAlchemyAtendimentoRepository(AtendimentoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, entity: Atendimento) -> Atendimento:
        model = await self.session.get(AtendimentoModel, entity.id)
        if model is None:
            model = AtendimentoModel(id=entity.id)
            self.session.add(model)
        model.codigo = entity.codigo
        model.beneficiario_id = entity.beneficiario_id
        model.tipo = entity.tipo.value
        model.descricao = entity.descricao
        model.responsavel_id = entity.responsavel_id
        model.data_atendimento = entity.data_atendimento
        model.status = entity.status.value
        model.encaminhamentos = entity.encaminhamentos
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, entity_id: UUID) -> Atendimento | None:
        model = await self.session.get(AtendimentoModel, entity_id)
        return self._to_domain(model) if model else None

    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[Atendimento]:
        stmt = select(AtendimentoModel).where(AtendimentoModel.beneficiario_id == beneficiario_id).order_by(AtendimentoModel.data_atendimento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[Atendimento]:
        stmt = select(AtendimentoModel).order_by(AtendimentoModel.data_atendimento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, entity_id: UUID) -> bool:
        model = await self.session.get(AtendimentoModel, entity_id)
        if model is None:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: AtendimentoModel) -> Atendimento:
        return Atendimento(id=model.id, codigo=model.codigo, beneficiario_id=model.beneficiario_id, tipo=TipoAtendimento(model.tipo), descricao=model.descricao, responsavel_id=model.responsavel_id, data_atendimento=model.data_atendimento, status=StatusAcompanhamento(model.status), encaminhamentos=model.encaminhamentos or [])