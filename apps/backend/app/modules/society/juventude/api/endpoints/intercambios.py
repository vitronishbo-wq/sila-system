from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.juventude.api.deps import get_intercambio_juvenil_service
from apps.backend.app.modules.society.juventude.api.schemas.intercambio_juvenil_schema import IntercambioJuvenilCreate, IntercambioJuvenilResponse, IntercambioJuvenilStatusUpdate
from apps.backend.app.modules.society.juventude.application.services.intercambio_juvenil_service import IntercambioJuvenilService
from apps.backend.app.modules.society.juventude.domain.enums import StatusIntercambio
router = APIRouter(prefix='/intercambios', tags=['Juventude - Intercambios'])

@router.post('/', response_model=IntercambioJuvenilResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_intercambio(data: IntercambioJuvenilCreate, service: IntercambioJuvenilService=Depends(get_intercambio_juvenil_service)) -> IntercambioJuvenilResponse:
    try:
        return await service.solicitar_intercambio(jovem_id=data.jovem_id, pais_destino=data.pais_destino, instituicao_destino=data.instituicao_destino, area_interesse=data.area_interesse, data_inicio=data.data_inicio, data_fim=data.data_fim, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{intercambio_id}', response_model=IntercambioJuvenilResponse)
async def obter_intercambio(intercambio_id: UUID, service: IntercambioJuvenilService=Depends(get_intercambio_juvenil_service)) -> IntercambioJuvenilResponse:
    try:
        return await service.buscar_intercambio(intercambio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[IntercambioJuvenilResponse])
async def listar_intercambios(jovem_id: UUID | None=None, status_filtro: StatusIntercambio | None=None, service: IntercambioJuvenilService=Depends(get_intercambio_juvenil_service)) -> list[IntercambioJuvenilResponse]:
    return await service.listar_intercambios(jovem_id=jovem_id, status=status_filtro)

@router.patch('/{intercambio_id}/status', response_model=IntercambioJuvenilResponse)
async def atualizar_status_intercambio(intercambio_id: UUID, data: IntercambioJuvenilStatusUpdate, service: IntercambioJuvenilService=Depends(get_intercambio_juvenil_service)) -> IntercambioJuvenilResponse:
    try:
        return await service.atualizar_status(intercambio_id=intercambio_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{intercambio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_intercambio(intercambio_id: UUID, service: IntercambioJuvenilService=Depends(get_intercambio_juvenil_service)) -> None:
    try:
        await service.remover_intercambio(intercambio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))