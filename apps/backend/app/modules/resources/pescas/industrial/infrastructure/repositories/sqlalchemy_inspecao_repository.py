from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.resources.pescas.industrial.application.ports.inspecao_sanitaria_industrial_repository_port import InspecaoSanitariaIndustrialRepositoryPort
from app.modules.resources.pescas.industrial.domain.enums import StatusInspecao, TipoSeloInspecao
from app.modules.resources.pescas.industrial.domain.models.inspecao_sanitaria_industrial import InspecaoSanitariaIndustrial
from app.modules.resources.pescas.industrial.infrastructure.models.inspecao_model import InspecaoModel

class SQLAlchemyInspecaoRepository(InspecaoSanitariaIndustrialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, inspecao: InspecaoSanitariaIndustrial) -> InspecaoSanitariaIndustrial:
        model = await self.session.get(InspecaoModel, inspecao.id)
        if not model:
            model = InspecaoModel(id=inspecao.id)
            self.session.add(model)
        model.codigo_inspecao = inspecao.codigo_inspecao
        model.unidade_processamento_id = inspecao.unidade_processamento_id
        model.data_agendada = inspecao.data_agendada
        model.selo_inspecao = inspecao.selo_inspecao.value
        model.status = inspecao.status.value
        model.fiscal_id = inspecao.fiscal_id
        model.lote_producao_id = inspecao.lote_producao_id
        model.data_realizacao = inspecao.data_realizacao
        model.pontuacao = inspecao.pontuacao
        model.inconformidades = list(inspecao.inconformidades) if inspecao.inconformidades else None
        model.observacoes = inspecao.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, inspecao_id: UUID) -> InspecaoSanitariaIndustrial | None:
        model = await self.session.get(InspecaoModel, inspecao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_inspecao: str) -> InspecaoSanitariaIndustrial | None:
        stmt = select(InspecaoModel).where(InspecaoModel.codigo_inspecao == codigo_inspecao.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[InspecaoSanitariaIndustrial]:
        stmt = select(InspecaoModel).order_by(InspecaoModel.codigo_inspecao.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[InspecaoSanitariaIndustrial]:
        stmt = select(InspecaoModel).where(InspecaoModel.unidade_processamento_id == unidade_processamento_id).order_by(InspecaoModel.codigo_inspecao.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusInspecao) -> list[InspecaoSanitariaIndustrial]:
        stmt = select(InspecaoModel).where(InspecaoModel.status == status.value).order_by(InspecaoModel.codigo_inspecao.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_lote(self, lote_producao_id: UUID) -> list[InspecaoSanitariaIndustrial]:
        stmt = select(InspecaoModel).where(InspecaoModel.lote_producao_id == lote_producao_id).order_by(InspecaoModel.codigo_inspecao.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[InspecaoSanitariaIndustrial]:
        stmt = select(InspecaoModel).where(InspecaoModel.data_agendada >= data_inicio).where(InspecaoModel.data_agendada <= data_fim).order_by(InspecaoModel.data_agendada.asc(), InspecaoModel.codigo_inspecao.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, inspecao_id: UUID) -> bool:
        model = await self.session.get(InspecaoModel, inspecao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(InspecaoModel).where(InspecaoModel.codigo_inspecao.like(f'INS/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'INS/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: InspecaoModel) -> InspecaoSanitariaIndustrial:
        return InspecaoSanitariaIndustrial(id=model.id, codigo_inspecao=model.codigo_inspecao, unidade_processamento_id=model.unidade_processamento_id, data_agendada=model.data_agendada, selo_inspecao=TipoSeloInspecao(model.selo_inspecao), status=StatusInspecao(model.status), fiscal_id=model.fiscal_id, lote_producao_id=model.lote_producao_id, data_realizacao=model.data_realizacao, pontuacao=model.pontuacao, inconformidades=list(model.inconformidades) if model.inconformidades else None, observacoes=model.observacoes)