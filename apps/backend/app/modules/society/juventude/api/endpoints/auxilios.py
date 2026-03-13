from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.society.juventude.api.deps import get_auxilio_service
from app.modules.society.juventude.api.schemas.auxilio_schema import AuxilioCreate, AuxilioResponse, AuxilioStatusUpdate
from app.modules.society.juventude.application.services.auxilio_service import AuxilioService
from app.modules.society.juventude.domain.enums import StatusBeneficio, TipoAuxilio
router = APIRouter(prefix='/auxilios', tags=['Juventude - Auxilios'])

@router.post('/', response_model=AuxilioResponse, status_code=status.HTTP_201_CREATED)
async def conceder_auxilio(data: AuxilioCreate, service: AuxilioService=Depends(get_auxilio_service)) -> AuxilioResponse:
    try:
        return await service.conceder_auxilio(jovem_id=data.jovem_id, tipo=data.tipo, data_inicio=data.data_inicio, valor_mensal=data.valor_mensal, data_fim=data.data_fim, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{auxilio_id}', response_model=AuxilioResponse)
async def obter_auxilio(auxilio_id: UUID, service: AuxilioService=Depends(get_auxilio_service)) -> AuxilioResponse:
    try:
        return await service.buscar_auxilio(auxilio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AuxilioResponse])
async def listar_auxilios(jovem_id: UUID | None=None, tipo: TipoAuxilio | None=None, status_filtro: StatusBeneficio | None=None, service: AuxilioService=Depends(get_auxilio_service)) -> list[AuxilioResponse]:
    return await service.listar_auxilios(jovem_id=jovem_id, tipo=tipo, status=status_filtro)

@router.patch('/{auxilio_id}/status', response_model=AuxilioResponse)
async def atualizar_status_auxilio(auxilio_id: UUID, data: AuxilioStatusUpdate, service: AuxilioService=Depends(get_auxilio_service)) -> AuxilioResponse:
    try:
        return await service.atualizar_status(auxilio_id=auxilio_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{auxilio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_auxilio(auxilio_id: UUID, service: AuxilioService=Depends(get_auxilio_service)) -> None:
    try:
        await service.remover_auxilio(auxilio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))