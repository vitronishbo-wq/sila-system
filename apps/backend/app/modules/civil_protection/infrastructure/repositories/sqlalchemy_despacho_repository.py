from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.civil_protection.application.ports.despacho_repository_port import DespachoRepositoryPort
from app.modules.civil_protection.domain.enums import StatusDespacho
from app.modules.civil_protection.domain.models.despacho import Despacho
from app.modules.civil_protection.infrastructure.models.despacho_model import DespachoModel

class SQLAlchemyDespachoRepository(DespachoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, despacho: Despacho) -> Despacho:
        model = await self.session.get(DespachoModel, despacho.id)
        if not model:
            model = DespachoModel(id=despacho.id)
            self.session.add(model)
        model.codigo_despacho = despacho.codigo_despacho
        model.ocorrencia_id = despacho.ocorrencia_id
        model.corporacao_id = despacho.corporacao_id
        model.bombeiro_responsavel_id = despacho.bombeiro_responsavel_id
        model.status = despacho.status.value
        model.data_despacho = despacho.data_despacho
        model.data_ultima_atualizacao = despacho.data_ultima_atualizacao
        model.meio_deslocamento = despacho.meio_deslocamento
        model.observacoes = despacho.observacoes
        model.ativo = despacho.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, despacho_id: UUID) -> Despacho | None:
        model = await self.session.get(DespachoModel, despacho_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_despacho: str) -> Despacho | None:
        stmt = select(DespachoModel).where(DespachoModel.codigo_despacho == codigo_despacho.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Despacho]:
        stmt = select(DespachoModel).order_by(DespachoModel.data_despacho.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Despacho]:
        stmt = select(DespachoModel).where(DespachoModel.ocorrencia_id == ocorrencia_id).order_by(DespachoModel.data_despacho.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusDespacho) -> list[Despacho]:
        stmt = select(DespachoModel).where(DespachoModel.status == status.value).order_by(DespachoModel.data_despacho.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, despacho_id: UUID) -> bool:
        model = await self.session.get(DespachoModel, despacho_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'DSP/{year}/'
        stmt = select(func.count()).select_from(DespachoModel).where(DespachoModel.codigo_despacho.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: DespachoModel) -> Despacho:
        return Despacho(id=model.id, codigo_despacho=model.codigo_despacho, ocorrencia_id=model.ocorrencia_id, corporacao_id=model.corporacao_id, status=StatusDespacho(model.status), data_despacho=model.data_despacho, data_ultima_atualizacao=model.data_ultima_atualizacao, bombeiro_responsavel_id=model.bombeiro_responsavel_id, meio_deslocamento=model.meio_deslocamento, observacoes=model.observacoes, ativo=model.ativo)