from __future__ import annotations
from fastapi import APIRouter, Depends, status
from app.modules.resources.pescas.api.deps import get_defeso_service
from app.modules.resources.pescas.api.schemas.defeso_schema import DefesoCreate, DefesoResponse
from app.modules.resources.pescas.application.services.defeso_service import DefesoService
router = APIRouter(prefix='/defesos', tags=['Pescas - Defesos'])

@router.post('/', response_model=DefesoResponse, status_code=status.HTTP_201_CREATED)
async def criar_defeso(data: DefesoCreate, service: DefesoService=Depends(get_defeso_service)):
    return await service.criar_defeso(periodo=data.periodo, especie_id=data.especie_id, data_inicio=data.data_inicio, data_fim=data.data_fim)

@router.get('/', response_model=list[DefesoResponse])
async def listar_defesos(service: DefesoService=Depends(get_defeso_service)):
    return await service.listar_defesos()