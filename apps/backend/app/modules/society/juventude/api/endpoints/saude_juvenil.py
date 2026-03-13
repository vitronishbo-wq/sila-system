from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.juventude.api.deps import get_saude_juvenil_service
from apps.backend.app.modules.society.juventude.api.schemas.saude_juvenil_schema import SaudeJuvenilCreate, SaudeJuvenilResponse, SaudeJuvenilStatusUpdate
from apps.backend.app.modules.society.juventude.application.services.saude_juvenil_service import SaudeJuvenilService
from apps.backend.app.modules.society.juventude.domain.enums import StatusAcompanhamento
router = APIRouter(prefix='/saude-juvenil', tags=['Juventude - Saude Juvenil'])

@router.post('/', response_model=SaudeJuvenilResponse, status_code=status.HTTP_201_CREATED)
async def registrar_saude(data: SaudeJuvenilCreate, service: SaudeJuvenilService=Depends(get_saude_juvenil_service)) -> SaudeJuvenilResponse:
    try:
        return await service.registrar_saude(jovem_id=data.jovem_id, tipo_registo=data.tipo_registo, descricao=data.descricao, data_registo=data.data_registo, encaminhamento_necessario=data.encaminhamento_necessario, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{registo_id}', response_model=SaudeJuvenilResponse)
async def obter_registo_saude(registo_id: UUID, service: SaudeJuvenilService=Depends(get_saude_juvenil_service)) -> SaudeJuvenilResponse:
    try:
        return await service.buscar_registo(registo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[SaudeJuvenilResponse])
async def listar_registos_saude(jovem_id: UUID | None=None, status_filtro: StatusAcompanhamento | None=None, service: SaudeJuvenilService=Depends(get_saude_juvenil_service)) -> list[SaudeJuvenilResponse]:
    return await service.listar_registos(jovem_id=jovem_id, status=status_filtro)

@router.patch('/{registo_id}/acompanhamento', response_model=SaudeJuvenilResponse)
async def atualizar_acompanhamento_saude(registo_id: UUID, data: SaudeJuvenilStatusUpdate, service: SaudeJuvenilService=Depends(get_saude_juvenil_service)) -> SaudeJuvenilResponse:
    try:
        return await service.atualizar_acompanhamento(registo_id=registo_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{registo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_registo_saude(registo_id: UUID, service: SaudeJuvenilService=Depends(get_saude_juvenil_service)) -> None:
    try:
        await service.remover_registo(registo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))