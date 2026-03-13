from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.public_security.application.ports.cadeia_custodia_repository_port import CadeiaCustodiaRepositoryPort
from apps.backend.app.modules.public_security.domain.enums import StatusCadeiaCustodia
from apps.backend.app.modules.public_security.domain.models.cadeia_custodia import CadeiaCustodia
from apps.backend.app.modules.public_security.infrastructure.models.cadeia_custodia_model import CadeiaCustodiaModel

class SQLAlchemyCadeiaCustodiaRepository(CadeiaCustodiaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, cadeia: CadeiaCustodia) -> CadeiaCustodia:
        model = await self.session.get(CadeiaCustodiaModel, cadeia.id)
        if not model:
            model = CadeiaCustodiaModel(id=cadeia.id)
            self.session.add(model)
        model.codigo_cadeia = cadeia.codigo_cadeia
        model.prova_id = cadeia.prova_id
        model.ocorrencia_id = cadeia.ocorrencia_id
        model.status = cadeia.status.value
        model.local_atual = cadeia.local_atual
        model.responsavel_id = cadeia.responsavel_id
        model.data_inicio = cadeia.data_inicio
        model.data_ultima_movimentacao = cadeia.data_ultima_movimentacao
        model.historico_movimentacoes = cadeia.historico_movimentacoes
        model.integridade_verificada = cadeia.integridade_verificada
        model.observacoes = cadeia.observacoes
        model.ativo = cadeia.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, cadeia_id: UUID) -> CadeiaCustodia | None:
        model = await self.session.get(CadeiaCustodiaModel, cadeia_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_cadeia: str) -> CadeiaCustodia | None:
        stmt = select(CadeiaCustodiaModel).where(CadeiaCustodiaModel.codigo_cadeia == codigo_cadeia.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_prova(self, prova_id: UUID) -> CadeiaCustodia | None:
        stmt = select(CadeiaCustodiaModel).where(CadeiaCustodiaModel.prova_id == prova_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[CadeiaCustodia]:
        stmt = select(CadeiaCustodiaModel).order_by(CadeiaCustodiaModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusCadeiaCustodia) -> list[CadeiaCustodia]:
        stmt = select(CadeiaCustodiaModel).where(CadeiaCustodiaModel.status == status.value).order_by(CadeiaCustodiaModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, cadeia_id: UUID) -> bool:
        model = await self.session.get(CadeiaCustodiaModel, cadeia_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'CCD/{year}/'
        stmt = select(func.count()).select_from(CadeiaCustodiaModel).where(CadeiaCustodiaModel.codigo_cadeia.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:06d}'

    @staticmethod
    def _to_domain(model: CadeiaCustodiaModel) -> CadeiaCustodia:
        return CadeiaCustodia(id=model.id, codigo_cadeia=model.codigo_cadeia, prova_id=model.prova_id, ocorrencia_id=model.ocorrencia_id, status=StatusCadeiaCustodia(model.status), local_atual=model.local_atual, responsavel_id=model.responsavel_id, data_inicio=model.data_inicio, data_ultima_movimentacao=model.data_ultima_movimentacao, historico_movimentacoes=model.historico_movimentacoes, integridade_verificada=model.integridade_verificada, observacoes=model.observacoes, ativo=model.ativo)