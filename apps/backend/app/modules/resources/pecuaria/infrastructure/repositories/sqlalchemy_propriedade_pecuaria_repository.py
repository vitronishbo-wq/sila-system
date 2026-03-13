from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pecuaria.application.ports import PropriedadePecuariaRepositoryPort
from apps.backend.app.modules.resources.pecuaria.domain.models.propriedade_pecuaria import PropriedadePecuaria
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.propriedade_pecuaria_model import PropriedadePecuariaModel

class SQLAlchemyPropriedadePecuariaRepository(PropriedadePecuariaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, item: PropriedadePecuaria) -> PropriedadePecuaria:
        model = await self.session.get(PropriedadePecuariaModel, item.id)
        if not model:
            model = PropriedadePecuariaModel(id=item.id)
            self.session.add(model)
        model.codigo_propriedade = item.codigo_propriedade
        model.pecuarista_id = item.pecuarista_id
        model.nome = item.nome
        model.area_total_ha = item.area_total_ha
        model.municipio = item.municipio
        model.provincia = item.provincia
        model.data_cadastro = item.data_cadastro
        model.ativo = item.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, propriedade_id: UUID) -> PropriedadePecuaria | None:
        model = await self.session.get(PropriedadePecuariaModel, propriedade_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_propriedade: str) -> PropriedadePecuaria | None:
        stmt = select(PropriedadePecuariaModel).where(PropriedadePecuariaModel.codigo_propriedade == codigo_propriedade)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_pecuarista(self, pecuarista_id: UUID | None=None) -> list[PropriedadePecuaria]:
        stmt = select(PropriedadePecuariaModel)
        if pecuarista_id:
            stmt = stmt.where(PropriedadePecuariaModel.pecuarista_id == pecuarista_id)
        rows = (await self.session.execute(stmt.order_by(PropriedadePecuariaModel.created_at.desc()))).scalars().all()
        return [self._to_domain(model) for model in rows]

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(PropriedadePecuariaModel).where(PropriedadePecuariaModel.codigo_propriedade.like(f'PROP/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'PROP/{ano}/{count + 1:06d}'

    @staticmethod
    def _to_domain(model: PropriedadePecuariaModel) -> PropriedadePecuaria:
        return PropriedadePecuaria(id=model.id, codigo_propriedade=model.codigo_propriedade, pecuarista_id=model.pecuarista_id, nome=model.nome, area_total_ha=model.area_total_ha, municipio=model.municipio, provincia=model.provincia, data_cadastro=model.data_cadastro, ativo=model.ativo)