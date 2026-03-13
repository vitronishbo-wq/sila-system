from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from app.modules.resources.florestas.application.ports.inventario_florestal_repository_port import InventarioFlorestalRepositoryPort
from app.modules.resources.florestas.domain.models.inventario_florestal import InventarioFlorestal

class InventarioService:

    def __init__(self, inventario_repo: InventarioFlorestalRepositoryPort):
        self.inventario_repo = inventario_repo

    async def registrar_inventario(self, *, unidade_manejo_id: UUID, volume_estimado_m3: Decimal, area_inventariada_ha: Decimal, observacoes: str | None=None) -> InventarioFlorestal:
        inventario = InventarioFlorestal.registrar(unidade_manejo_id=unidade_manejo_id, volume_estimado_m3=volume_estimado_m3, area_inventariada_ha=area_inventariada_ha, observacoes=observacoes)
        return await self.inventario_repo.save(inventario)

    async def listar_inventarios(self, unidade_manejo_id: UUID) -> list[InventarioFlorestal]:
        return await self.inventario_repo.list_by_unidade(unidade_manejo_id)