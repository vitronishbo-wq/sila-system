from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends
from apps.backend.app.modules.resources.florestas.api.deps import get_inventario_service
from apps.backend.app.modules.resources.florestas.api.schemas.inventario_florestal_schema import InventarioFlorestalCreate, InventarioFlorestalResponse
from apps.backend.app.modules.resources.florestas.application.services.inventario_service import InventarioService
router = APIRouter(prefix='/inventarios', tags=['Florestas - Inventarios'])

@router.post('/', response_model=InventarioFlorestalResponse, status_code=201)
async def registrar_inventario(data: InventarioFlorestalCreate, service: InventarioService=Depends(get_inventario_service)):
    return await service.registrar_inventario(unidade_manejo_id=data.unidade_manejo_id, volume_estimado_m3=data.volume_estimado_m3, area_inventariada_ha=data.area_inventariada_ha, observacoes=data.observacoes)

@router.get('/', response_model=list[InventarioFlorestalResponse])
async def listar_inventarios(unidade_manejo_id: UUID, service: InventarioService=Depends(get_inventario_service)):
    return await service.listar_inventarios(unidade_manejo_id)