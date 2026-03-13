from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.resources.pecuaria.application.ports import RebanhoRepositoryPort
from app.modules.resources.pecuaria.domain.enums import StatusRebanho, TipoAnimal
from app.modules.resources.pecuaria.domain.models.rebanho import Rebanho
from app.modules.resources.pecuaria.infrastructure.models.rebanho_model import RebanhoModel

class SQLAlchemyRebanhoRepository(RebanhoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, item: Rebanho) -> Rebanho:
        model = await self.session.get(RebanhoModel, item.id)
        if not model:
            model = RebanhoModel(id=item.id)
            self.session.add(model)
        model.codigo_rebanho = item.codigo_rebanho
        model.propriedade_id = item.propriedade_id
        model.tipo_animal = item.tipo_animal.value
        model.descricao = item.descricao
        model.quantidade_animais = item.quantidade_animais
        model.data_cadastro = item.data_cadastro
        model.status = item.status.value
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, rebanho_id: UUID) -> Rebanho | None:
        model = await self.session.get(RebanhoModel, rebanho_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_rebanho: str) -> Rebanho | None:
        stmt = select(RebanhoModel).where(RebanhoModel.codigo_rebanho == codigo_rebanho)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_propriedade(self, propriedade_id: UUID | None=None) -> list[Rebanho]:
        stmt = select(RebanhoModel)
        if propriedade_id:
            stmt = stmt.where(RebanhoModel.propriedade_id == propriedade_id)
        rows = (await self.session.execute(stmt.order_by(RebanhoModel.created_at.desc()))).scalars().all()
        return [self._to_domain(model) for model in rows]

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(RebanhoModel).where(RebanhoModel.codigo_rebanho.like(f'REB/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'REB/{ano}/{count + 1:06d}'

    @staticmethod
    def _to_domain(model: RebanhoModel) -> Rebanho:
        return Rebanho(id=model.id, codigo_rebanho=model.codigo_rebanho, propriedade_id=model.propriedade_id, tipo_animal=TipoAnimal(model.tipo_animal), descricao=model.descricao, quantidade_animais=model.quantidade_animais, data_cadastro=model.data_cadastro, status=StatusRebanho(model.status))