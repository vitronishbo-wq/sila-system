from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.juventude.application.ports.acompanhamento_juvenil_repository_port import AcompanhamentoJuvenilRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import StatusAcompanhamento
from apps.backend.app.modules.society.juventude.domain.models.acompanhamento_juvenil import AcompanhamentoJuvenil
from apps.backend.app.modules.society.juventude.infrastructure.models.acompanhamento_juvenil_model import AcompanhamentoJuvenilModel

class SQLAlchemyAcompanhamentoJuvenilRepository(AcompanhamentoJuvenilRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, acompanhamento: AcompanhamentoJuvenil) -> AcompanhamentoJuvenil:
        model = await self.session.get(AcompanhamentoJuvenilModel, acompanhamento.id)
        if not model:
            model = AcompanhamentoJuvenilModel(id=acompanhamento.id)
            self.session.add(model)
        model.codigo_acompanhamento = acompanhamento.codigo_acompanhamento
        model.jovem_id = acompanhamento.jovem_id
        model.responsavel = acompanhamento.responsavel
        model.objetivo = acompanhamento.objetivo
        model.data_inicio = acompanhamento.data_inicio
        model.data_registo = acompanhamento.data_registo
        model.status = acompanhamento.status.value
        model.proxima_revisao = acompanhamento.proxima_revisao
        model.historico = acompanhamento.historico
        model.observacoes = acompanhamento.observacoes
        model.ativo = acompanhamento.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, acompanhamento_id: UUID) -> AcompanhamentoJuvenil | None:
        model = await self.session.get(AcompanhamentoJuvenilModel, acompanhamento_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_acompanhamento: str) -> AcompanhamentoJuvenil | None:
        stmt = select(AcompanhamentoJuvenilModel).where(AcompanhamentoJuvenilModel.codigo_acompanhamento == codigo_acompanhamento.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[AcompanhamentoJuvenil]:
        stmt = select(AcompanhamentoJuvenilModel).order_by(AcompanhamentoJuvenilModel.data_registo.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[AcompanhamentoJuvenil]:
        stmt = select(AcompanhamentoJuvenilModel).where(AcompanhamentoJuvenilModel.jovem_id == jovem_id).order_by(AcompanhamentoJuvenilModel.data_registo.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusAcompanhamento) -> list[AcompanhamentoJuvenil]:
        stmt = select(AcompanhamentoJuvenilModel).where(AcompanhamentoJuvenilModel.status == status.value).order_by(AcompanhamentoJuvenilModel.data_registo.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, acompanhamento_id: UUID) -> bool:
        model = await self.session.get(AcompanhamentoJuvenilModel, acompanhamento_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(AcompanhamentoJuvenilModel).where(AcompanhamentoJuvenilModel.codigo_acompanhamento.like(f'ACP/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'ACP/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: AcompanhamentoJuvenilModel) -> AcompanhamentoJuvenil:
        return AcompanhamentoJuvenil(id=model.id, codigo_acompanhamento=model.codigo_acompanhamento, jovem_id=model.jovem_id, responsavel=model.responsavel, objetivo=model.objetivo, data_inicio=model.data_inicio, data_registo=model.data_registo or date.today(), status=StatusAcompanhamento(model.status), proxima_revisao=model.proxima_revisao, historico=model.historico, observacoes=model.observacoes, ativo=model.ativo)