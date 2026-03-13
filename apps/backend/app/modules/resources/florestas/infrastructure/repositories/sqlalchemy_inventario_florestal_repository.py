from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.florestas.application.ports.inventario_florestal_repository_port import InventarioFlorestalRepositoryPort
from apps.backend.app.modules.resources.florestas.domain.models.inventario_florestal import InventarioFlorestal
from apps.backend.app.modules.resources.florestas.infrastructure.models.inventario_florestal_model import InventarioFlorestalModel

class SQLAlchemyInventarioFlorestalRepository(InventarioFlorestalRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, inventario: InventarioFlorestal) -> InventarioFlorestal:
        model = await self.session.get(InventarioFlorestalModel, inventario.id)
        if not model:
            model = InventarioFlorestalModel(id=inventario.id)
            self.session.add(model)
        model.unidade_manejo_id = inventario.unidade_manejo_id
        model.data_inventario = inventario.data_inventario
        model.volume_estimado_m3 = inventario.volume_estimado_m3
        model.area_inventariada_ha = inventario.area_inventariada_ha
        model.status = inventario.status
        model.observacoes = inventario.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, inventario_id: UUID) -> InventarioFlorestal | None:
        model = await self.session.get(InventarioFlorestalModel, inventario_id)
        return self._to_domain(model) if model else None

    async def list_by_unidade(self, unidade_manejo_id: UUID) -> list[InventarioFlorestal]:
        stmt = select(InventarioFlorestalModel).where(InventarioFlorestalModel.unidade_manejo_id == unidade_manejo_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(model: InventarioFlorestalModel) -> InventarioFlorestal:
        return InventarioFlorestal(id=model.id, unidade_manejo_id=model.unidade_manejo_id, data_inventario=model.data_inventario, volume_estimado_m3=model.volume_estimado_m3, area_inventariada_ha=model.area_inventariada_ha, status=model.status, observacoes=model.observacoes)
SqlalchemyInventarioFlorestalRepository = SQLAlchemyInventarioFlorestalRepository