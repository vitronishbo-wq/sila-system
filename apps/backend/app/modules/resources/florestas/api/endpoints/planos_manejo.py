from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from apps.backend.app.modules.resources.florestas.api.deps import get_plano_manejo_service
from apps.backend.app.modules.resources.florestas.api.schemas.plano_manejo_florestal_schema import PlanoManejoCreate, PlanoManejoResponse
from apps.backend.app.modules.resources.florestas.application.services.plano_manejo_service import PlanoManejoService
router = APIRouter(prefix='/planos-manejo', tags=['Florestas - Planos Manejo'])

@router.post('/', response_model=PlanoManejoResponse, status_code=201)
async def submeter_plano(data: PlanoManejoCreate, service: PlanoManejoService=Depends(get_plano_manejo_service)):
    try:
        return await service.submeter_plano(unidade_manejo_id=data.unidade_manejo_id, responsavel_tecnico_id=data.responsavel_tecnico_id, responsavel_tecnico_registro=data.responsavel_tecnico_registro, volume_anual_estimado_m3=data.volume_anual_estimado_m3, ciclo_corte_anos=data.ciclo_corte_anos, area_anual_ha=data.area_anual_ha)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get('/', response_model=list[PlanoManejoResponse])
async def listar_planos(unidade_manejo_id: UUID, service: PlanoManejoService=Depends(get_plano_manejo_service)):
    return await service.listar_planos(unidade_manejo_id)