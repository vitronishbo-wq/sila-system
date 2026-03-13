from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_infraestrutura_service
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.infraestrutura_schema import InfraestruturaCreate, InfraestruturaResponse, InfraestruturaStatusUpdate
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.infraestrutura_service import InfraestruturaService
router = APIRouter(prefix='/infraestruturas', tags=['Telecomunicacoes - Infraestruturas'])

@router.post('/', response_model=InfraestruturaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_infraestrutura(data: InfraestruturaCreate, service: InfraestruturaService=Depends(get_infraestrutura_service)) -> InfraestruturaResponse:
    try:
        return await service.cadastrar_infraestrutura(operadora_id=data.operadora_id, tipo=data.tipo, identificador=data.identificador, municipio=data.municipio, provincia=data.provincia, data_implantacao=data.data_implantacao, latitude=data.latitude, longitude=data.longitude, capacidade=data.capacidade, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{infraestrutura_id}', response_model=InfraestruturaResponse)
async def obter_infraestrutura(infraestrutura_id: UUID, service: InfraestruturaService=Depends(get_infraestrutura_service)) -> InfraestruturaResponse:
    try:
        return await service.buscar_infraestrutura(infraestrutura_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[InfraestruturaResponse])
async def listar_infraestruturas(operadora_id: UUID | None=None, municipio: str | None=None, somente_ativas: bool=False, service: InfraestruturaService=Depends(get_infraestrutura_service)) -> list[InfraestruturaResponse]:
    return await service.listar_infraestruturas(operadora_id=operadora_id, municipio=municipio, somente_ativas=somente_ativas)

@router.patch('/{infraestrutura_id}/status', response_model=InfraestruturaResponse)
async def atualizar_status_infraestrutura(infraestrutura_id: UUID, data: InfraestruturaStatusUpdate, service: InfraestruturaService=Depends(get_infraestrutura_service)) -> InfraestruturaResponse:
    try:
        return await service.atualizar_status(infraestrutura_id=infraestrutura_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{infraestrutura_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_infraestrutura(infraestrutura_id: UUID, service: InfraestruturaService=Depends(get_infraestrutura_service)) -> None:
    try:
        await service.remover_infraestrutura(infraestrutura_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))