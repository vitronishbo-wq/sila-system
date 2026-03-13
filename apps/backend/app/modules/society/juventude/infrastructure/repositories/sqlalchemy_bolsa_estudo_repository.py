from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.juventude.application.ports.bolsa_estudo_repository_port import BolsaEstudoRepositoryPort
from app.modules.society.juventude.domain.enums import TipoBolsa
from app.modules.society.juventude.domain.models.bolsa_estudo import BolsaEstudo
from app.modules.society.juventude.infrastructure.models.bolsa_estudo_model import BolsaEstudoModel

class SQLAlchemyBolsaEstudoRepository(BolsaEstudoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, bolsa: BolsaEstudo) -> BolsaEstudo:
        model = await self.session.get(BolsaEstudoModel, bolsa.id)
        if not model:
            model = BolsaEstudoModel(id=bolsa.id)
            self.session.add(model)
        model.codigo_bolsa = bolsa.codigo_bolsa
        model.jovem_id = bolsa.jovem_id
        model.tipo = bolsa.tipo.value
        model.valor_mensal = bolsa.valor_mensal
        model.data_inicio = bolsa.data_inicio
        model.data_fim = bolsa.data_fim
        model.data_cadastro = bolsa.data_cadastro
        model.observacoes = bolsa.observacoes
        model.ativa = bolsa.ativa
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, bolsa_id: UUID) -> BolsaEstudo | None:
        model = await self.session.get(BolsaEstudoModel, bolsa_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_bolsa: str) -> BolsaEstudo | None:
        stmt = select(BolsaEstudoModel).where(BolsaEstudoModel.codigo_bolsa == codigo_bolsa.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[BolsaEstudo]:
        stmt = select(BolsaEstudoModel).order_by(BolsaEstudoModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[BolsaEstudo]:
        stmt = select(BolsaEstudoModel).where(BolsaEstudoModel.jovem_id == jovem_id).order_by(BolsaEstudoModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_ativas(self) -> list[BolsaEstudo]:
        stmt = select(BolsaEstudoModel).where(BolsaEstudoModel.ativa.is_(True)).order_by(BolsaEstudoModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, bolsa_id: UUID) -> bool:
        model = await self.session.get(BolsaEstudoModel, bolsa_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(BolsaEstudoModel).where(BolsaEstudoModel.codigo_bolsa.like(f'BOL/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'BOL/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: BolsaEstudoModel) -> BolsaEstudo:
        return BolsaEstudo(id=model.id, codigo_bolsa=model.codigo_bolsa, jovem_id=model.jovem_id, tipo=TipoBolsa(model.tipo), valor_mensal=model.valor_mensal, data_inicio=model.data_inicio, data_fim=model.data_fim, data_cadastro=model.data_cadastro, observacoes=model.observacoes, ativa=model.ativa)