from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.resources.florestas.application.ports.concessionario_florestal_repository_port import ConcessionarioFlorestalRepositoryPort
from app.modules.resources.florestas.domain.enums import TipoOperadorFlorestal
from app.modules.resources.florestas.domain.models.concessionario_florestal import ConcessionarioFlorestal
from app.modules.resources.florestas.infrastructure.models.operador_florestal_model import OperadorFlorestalModel

class SQLAlchemyOperadorFlorestalRepository(ConcessionarioFlorestalRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, operador: ConcessionarioFlorestal) -> ConcessionarioFlorestal:
        model = await self.session.get(OperadorFlorestalModel, operador.id)
        if not model:
            model = OperadorFlorestalModel(id=operador.id)
            self.session.add(model)
        model.nome = operador.nome
        model.nif = operador.nif
        model.tipo_operador = operador.tipo_operador.value
        model.data_registro = operador.data_registro
        model.ativo = operador.ativo
        model.observacoes = operador.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, operador_id: UUID) -> ConcessionarioFlorestal | None:
        model = await self.session.get(OperadorFlorestalModel, operador_id)
        return self._to_domain(model) if model else None

    async def get_by_nif(self, nif: str) -> ConcessionarioFlorestal | None:
        stmt = select(OperadorFlorestalModel).where(OperadorFlorestalModel.nif == nif)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self, ativo: bool | None=None) -> list[ConcessionarioFlorestal]:
        stmt = select(OperadorFlorestalModel)
        if ativo is not None:
            stmt = stmt.where(OperadorFlorestalModel.ativo == ativo)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(model: OperadorFlorestalModel) -> ConcessionarioFlorestal:
        return ConcessionarioFlorestal(id=model.id, nome=model.nome, nif=model.nif, tipo_operador=TipoOperadorFlorestal(model.tipo_operador), data_registro=model.data_registro, ativo=model.ativo, observacoes=model.observacoes)
SqlalchemyOperadorFlorestalRepository = SQLAlchemyOperadorFlorestalRepository