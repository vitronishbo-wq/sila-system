from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.juventude.api.deps import get_empreendedorismo_juvenil_service
from apps.backend.app.modules.society.juventude.api.schemas.empreendedorismo_juvenil_schema import EmpreendedorismoJuvenilCreate, EmpreendedorismoJuvenilResponse, EmpreendedorismoJuvenilStatusUpdate
from apps.backend.app.modules.society.juventude.application.services.empreendedorismo_juvenil_service import EmpreendedorismoJuvenilService
from apps.backend.app.modules.society.juventude.domain.enums import StatusEmpreendimento
router = APIRouter(prefix='/empreendedorismo-juvenil', tags=['Juventude - Empreendedorismo'])

@router.post('/', response_model=EmpreendedorismoJuvenilResponse, status_code=status.HTTP_201_CREATED)
async def registrar_empreendimento(data: EmpreendedorismoJuvenilCreate, service: EmpreendedorismoJuvenilService=Depends(get_empreendedorismo_juvenil_service)) -> EmpreendedorismoJuvenilResponse:
    try:
        return await service.registrar_empreendimento(jovem_id=data.jovem_id, nome_negocio=data.nome_negocio, area_interesse=data.area_interesse, receita_mensal=data.receita_mensal, valor_credito=data.valor_credito, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{empreendimento_id}', response_model=EmpreendedorismoJuvenilResponse)
async def obter_empreendimento(empreendimento_id: UUID, service: EmpreendedorismoJuvenilService=Depends(get_empreendedorismo_juvenil_service)) -> EmpreendedorismoJuvenilResponse:
    try:
        return await service.buscar_empreendimento(empreendimento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EmpreendedorismoJuvenilResponse])
async def listar_empreendimentos(jovem_id: UUID | None=None, status_filtro: StatusEmpreendimento | None=None, service: EmpreendedorismoJuvenilService=Depends(get_empreendedorismo_juvenil_service)) -> list[EmpreendedorismoJuvenilResponse]:
    return await service.listar_empreendimentos(jovem_id=jovem_id, status=status_filtro)

@router.patch('/{empreendimento_id}/status', response_model=EmpreendedorismoJuvenilResponse)
async def atualizar_status_empreendimento(empreendimento_id: UUID, data: EmpreendedorismoJuvenilStatusUpdate, service: EmpreendedorismoJuvenilService=Depends(get_empreendedorismo_juvenil_service)) -> EmpreendedorismoJuvenilResponse:
    try:
        return await service.atualizar_status(empreendimento_id=empreendimento_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{empreendimento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_empreendimento(empreendimento_id: UUID, service: EmpreendedorismoJuvenilService=Depends(get_empreendedorismo_juvenil_service)) -> None:
    try:
        await service.remover_empreendimento(empreendimento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))