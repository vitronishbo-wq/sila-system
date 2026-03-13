from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.pescas.api.deps import get_pescador_service
from apps.backend.app.modules.resources.pescas.api.schemas.pescador_schema import PescadorCreate, PescadorFilter, PescadorResponse
from apps.backend.app.modules.resources.pescas.application.services.pescador_service import PescadorService
router = APIRouter(prefix='/pescadores', tags=['Pescas - Pescadores'])

@router.post('/', response_model=PescadorResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_pescador(data: PescadorCreate, service: PescadorService=Depends(get_pescador_service)):
    try:
        return await service.cadastrar_pescador(nome=data.nome, tipo=data.tipo, citizen_id=data.citizen_id, numero_registro=data.numero_registro)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{pescador_id}', response_model=PescadorResponse)
async def obter_pescador(pescador_id: UUID, service: PescadorService=Depends(get_pescador_service)):
    try:
        return await service.buscar_pescador(pescador_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[PescadorResponse])
async def listar_pescadores(filtros: PescadorFilter=Depends(), service: PescadorService=Depends(get_pescador_service)):
    return await service.listar_pescadores(tipo=filtros.tipo)