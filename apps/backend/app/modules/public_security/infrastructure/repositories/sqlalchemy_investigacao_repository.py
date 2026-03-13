from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.public_security.application.ports.investigacao_repository_port import InvestigacaoRepositoryPort
from apps.backend.app.modules.public_security.domain.enums import StatusInvestigacao
from apps.backend.app.modules.public_security.domain.models.investigacao import Investigacao
from apps.backend.app.modules.public_security.infrastructure.models.investigacao_model import InvestigacaoModel

class SQLAlchemyInvestigacaoRepository(InvestigacaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, investigacao: Investigacao) -> Investigacao:
        model = await self.session.get(InvestigacaoModel, investigacao.id)
        if not model:
            model = InvestigacaoModel(id=investigacao.id)
            self.session.add(model)
        model.codigo_investigacao = investigacao.codigo_investigacao
        model.ocorrencia_id = investigacao.ocorrencia_id
        model.unidade_id = investigacao.unidade_id
        model.data_abertura = investigacao.data_abertura
        model.status = investigacao.status.value
        model.delegado_responsavel_id = investigacao.delegado_responsavel_id
        model.data_conclusao = investigacao.data_conclusao
        model.resumo = investigacao.resumo
        model.observacoes = investigacao.observacoes
        model.ativo = investigacao.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, investigacao_id: UUID) -> Investigacao | None:
        model = await self.session.get(InvestigacaoModel, investigacao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_investigacao: str) -> Investigacao | None:
        stmt = select(InvestigacaoModel).where(InvestigacaoModel.codigo_investigacao == codigo_investigacao.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Investigacao]:
        stmt = select(InvestigacaoModel).order_by(InvestigacaoModel.data_abertura.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Investigacao]:
        stmt = select(InvestigacaoModel).where(InvestigacaoModel.ocorrencia_id == ocorrencia_id).order_by(InvestigacaoModel.data_abertura.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusInvestigacao) -> list[Investigacao]:
        stmt = select(InvestigacaoModel).where(InvestigacaoModel.status == status.value).order_by(InvestigacaoModel.data_abertura.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, investigacao_id: UUID) -> bool:
        model = await self.session.get(InvestigacaoModel, investigacao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'INV/{year}/'
        stmt = select(func.count()).select_from(InvestigacaoModel).where(InvestigacaoModel.codigo_investigacao.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: InvestigacaoModel) -> Investigacao:
        return Investigacao(id=model.id, codigo_investigacao=model.codigo_investigacao, ocorrencia_id=model.ocorrencia_id, unidade_id=model.unidade_id, data_abertura=model.data_abertura, status=StatusInvestigacao(model.status), delegado_responsavel_id=model.delegado_responsavel_id, data_conclusao=model.data_conclusao, resumo=model.resumo, observacoes=model.observacoes, ativo=model.ativo)