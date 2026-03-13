from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.juventude.application.ports.intercambio_juvenil_repository_port import IntercambioJuvenilRepositoryPort
from app.modules.society.juventude.domain.enums import AreaInteresse, StatusIntercambio
from app.modules.society.juventude.domain.models.intercambio_juvenil import IntercambioJuvenil
from app.modules.society.juventude.infrastructure.models.intercambio_juvenil_model import IntercambioJuvenilModel

class SQLAlchemyIntercambioJuvenilRepository(IntercambioJuvenilRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, intercambio: IntercambioJuvenil) -> IntercambioJuvenil:
        model = await self.session.get(IntercambioJuvenilModel, intercambio.id)
        if not model:
            model = IntercambioJuvenilModel(id=intercambio.id)
            self.session.add(model)
        model.codigo_intercambio = intercambio.codigo_intercambio
        model.jovem_id = intercambio.jovem_id
        model.pais_destino = intercambio.pais_destino
        model.instituicao_destino = intercambio.instituicao_destino
        model.area_interesse = intercambio.area_interesse.value
        model.data_inicio = intercambio.data_inicio
        model.data_fim = intercambio.data_fim
        model.status = intercambio.status.value
        model.data_cadastro = intercambio.data_cadastro
        model.observacoes = intercambio.observacoes
        model.ativo = intercambio.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, intercambio_id: UUID) -> IntercambioJuvenil | None:
        model = await self.session.get(IntercambioJuvenilModel, intercambio_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_intercambio: str) -> IntercambioJuvenil | None:
        stmt = select(IntercambioJuvenilModel).where(IntercambioJuvenilModel.codigo_intercambio == codigo_intercambio.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[IntercambioJuvenil]:
        stmt = select(IntercambioJuvenilModel).order_by(IntercambioJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[IntercambioJuvenil]:
        stmt = select(IntercambioJuvenilModel).where(IntercambioJuvenilModel.jovem_id == jovem_id).order_by(IntercambioJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusIntercambio) -> list[IntercambioJuvenil]:
        stmt = select(IntercambioJuvenilModel).where(IntercambioJuvenilModel.status == status.value).order_by(IntercambioJuvenilModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, intercambio_id: UUID) -> bool:
        model = await self.session.get(IntercambioJuvenilModel, intercambio_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(IntercambioJuvenilModel).where(IntercambioJuvenilModel.codigo_intercambio.like(f'INT/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'INT/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: IntercambioJuvenilModel) -> IntercambioJuvenil:
        return IntercambioJuvenil(id=model.id, codigo_intercambio=model.codigo_intercambio, jovem_id=model.jovem_id, pais_destino=model.pais_destino, instituicao_destino=model.instituicao_destino, area_interesse=AreaInteresse(model.area_interesse), data_inicio=model.data_inicio, data_fim=model.data_fim, status=StatusIntercambio(model.status), data_cadastro=model.data_cadastro, observacoes=model.observacoes, ativo=model.ativo)