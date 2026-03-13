from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.resources.pescas.application.ports import PescadorRepositoryPort
from app.modules.resources.pescas.domain.enums import TipoPescador
from app.modules.resources.pescas.domain.models.pescador import Pescador
from app.modules.resources.pescas.infrastructure.models.pescador_model import PescadorModel

class SQLAlchemyPescadorRepository(PescadorRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, pescador: Pescador) -> Pescador:
        model = await self.session.get(PescadorModel, pescador.id)
        if not model:
            model = PescadorModel(id=pescador.id)
            self.session.add(model)
        model.nome = pescador.nome
        model.numero_registro = pescador.numero_registro
        model.tipo = pescador.tipo.value
        model.citizen_id = pescador.citizen_id
        model.data_registro = pescador.data_registro
        model.ativo = pescador.ativo
        model.telefone = pescador.telefone
        model.email = pescador.email
        model.cooperativa_id = pescador.cooperativa_id
        model.observacoes = pescador.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, pescador_id: UUID) -> Pescador | None:
        model = await self.session.get(PescadorModel, pescador_id)
        return self._to_domain(model) if model else None

    async def get_by_numero_registro(self, numero_registro: str) -> Pescador | None:
        stmt = select(PescadorModel).where(PescadorModel.numero_registro == numero_registro)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_tipo(self, tipo: TipoPescador | None=None) -> list[Pescador]:
        stmt = select(PescadorModel)
        if tipo:
            stmt = stmt.where(PescadorModel.tipo == tipo.value)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_registro(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(PescadorModel).where(PescadorModel.numero_registro.like(f'PES/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'PES/{ano}/{count + 1:06d}'

    @staticmethod
    def _to_domain(model: PescadorModel) -> Pescador:
        return Pescador(id=model.id, nome=model.nome, numero_registro=model.numero_registro, tipo=TipoPescador(model.tipo), citizen_id=model.citizen_id, data_registro=model.data_registro, ativo=model.ativo, telefone=model.telefone, email=model.email, cooperativa_id=model.cooperativa_id, observacoes=model.observacoes)