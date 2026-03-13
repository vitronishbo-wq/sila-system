from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pescas.industrial.application.ports.lote_producao_repository_port import LoteProducaoRepositoryPort
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import MercadoDestino, StatusLoteProducao
from apps.backend.app.modules.resources.pescas.industrial.domain.models.lote_producao import LoteProducao
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.lote_producao_model import LoteProducaoModel

class SQLAlchemyLoteProducaoRepository(LoteProducaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, lote: LoteProducao) -> LoteProducao:
        model = await self.session.get(LoteProducaoModel, lote.id)
        if not model:
            model = LoteProducaoModel(id=lote.id)
            self.session.add(model)
        model.codigo_lote = lote.codigo_lote
        model.unidade_processamento_id = lote.unidade_processamento_id
        model.produto_processado_id = lote.produto_processado_id
        model.data_producao = lote.data_producao
        model.quantidade_kg = lote.quantidade_kg
        model.status = lote.status.value
        model.destino_mercado = lote.destino_mercado.value
        model.data_validade = lote.data_validade
        model.turno = lote.turno
        model.temperatura_armazenamento_c = lote.temperatura_armazenamento_c
        model.observacoes = lote.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, lote_id: UUID) -> LoteProducao | None:
        model = await self.session.get(LoteProducaoModel, lote_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_lote: str) -> LoteProducao | None:
        stmt = select(LoteProducaoModel).where(LoteProducaoModel.codigo_lote == codigo_lote.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[LoteProducao]:
        stmt = select(LoteProducaoModel).order_by(LoteProducaoModel.codigo_lote.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[LoteProducao]:
        stmt = select(LoteProducaoModel).where(LoteProducaoModel.unidade_processamento_id == unidade_processamento_id).order_by(LoteProducaoModel.codigo_lote.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_produto(self, produto_processado_id: UUID) -> list[LoteProducao]:
        stmt = select(LoteProducaoModel).where(LoteProducaoModel.produto_processado_id == produto_processado_id).order_by(LoteProducaoModel.codigo_lote.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusLoteProducao) -> list[LoteProducao]:
        stmt = select(LoteProducaoModel).where(LoteProducaoModel.status == status.value).order_by(LoteProducaoModel.codigo_lote.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[LoteProducao]:
        stmt = select(LoteProducaoModel).where(LoteProducaoModel.data_producao >= data_inicio).where(LoteProducaoModel.data_producao <= data_fim).order_by(LoteProducaoModel.data_producao.asc(), LoteProducaoModel.codigo_lote.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, lote_id: UUID) -> bool:
        model = await self.session.get(LoteProducaoModel, lote_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(LoteProducaoModel).where(LoteProducaoModel.codigo_lote.like(f'LOT/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'LOT/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: LoteProducaoModel) -> LoteProducao:
        return LoteProducao(id=model.id, codigo_lote=model.codigo_lote, unidade_processamento_id=model.unidade_processamento_id, produto_processado_id=model.produto_processado_id, data_producao=model.data_producao, quantidade_kg=model.quantidade_kg, status=StatusLoteProducao(model.status), destino_mercado=MercadoDestino(model.destino_mercado), data_validade=model.data_validade, turno=model.turno, temperatura_armazenamento_c=model.temperatura_armazenamento_c, observacoes=model.observacoes)