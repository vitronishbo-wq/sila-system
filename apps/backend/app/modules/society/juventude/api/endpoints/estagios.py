from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.juventude.api.deps import get_estagio_juvenil_service
from apps.backend.app.modules.society.juventude.api.schemas.estagio_juvenil_schema import EstagioJuvenilCreate, EstagioJuvenilResponse, EstagioJuvenilStatusUpdate
from apps.backend.app.modules.society.juventude.application.services.estagio_juvenil_service import EstagioJuvenilService
from apps.backend.app.modules.society.juventude.domain.enums import StatusEstagio
router = APIRouter(prefix='/estagios', tags=['Juventude - Estagios'])

@router.post('/', response_model=EstagioJuvenilResponse, status_code=status.HTTP_201_CREATED)
async def registrar_estagio(data: EstagioJuvenilCreate, service: EstagioJuvenilService=Depends(get_estagio_juvenil_service)) -> EstagioJuvenilResponse:
    try:
        return await service.registrar_estagio(jovem_id=data.jovem_id, instituicao=data.instituicao, area_interesse=data.area_interesse, cargo=data.cargo, carga_horaria_semanal=data.carga_horaria_semanal, data_inicio=data.data_inicio, bolsa_auxilio=data.bolsa_auxilio, data_fim=data.data_fim, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{estagio_id}', response_model=EstagioJuvenilResponse)
async def obter_estagio(estagio_id: UUID, service: EstagioJuvenilService=Depends(get_estagio_juvenil_service)) -> EstagioJuvenilResponse:
    try:
        return await service.buscar_estagio(estagio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EstagioJuvenilResponse])
async def listar_estagios(jovem_id: UUID | None=None, status_filtro: StatusEstagio | None=None, service: EstagioJuvenilService=Depends(get_estagio_juvenil_service)) -> list[EstagioJuvenilResponse]:
    return await service.listar_estagios(jovem_id=jovem_id, status=status_filtro)

@router.patch('/{estagio_id}/status', response_model=EstagioJuvenilResponse)
async def atualizar_status_estagio(estagio_id: UUID, data: EstagioJuvenilStatusUpdate, service: EstagioJuvenilService=Depends(get_estagio_juvenil_service)) -> EstagioJuvenilResponse:
    try:
        return await service.atualizar_status(estagio_id=estagio_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{estagio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_estagio(estagio_id: UUID, service: EstagioJuvenilService=Depends(get_estagio_juvenil_service)) -> None:
    try:
        await service.remover_estagio(estagio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))