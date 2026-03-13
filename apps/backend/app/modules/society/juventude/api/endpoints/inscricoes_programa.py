from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.society.juventude.api.deps import get_inscricao_programa_service
from app.modules.society.juventude.api.schemas.inscricao_programa_schema import InscricaoProgramaCancelar, InscricaoProgramaCreate, InscricaoProgramaResponse
from app.modules.society.juventude.application.services.inscricao_programa_service import InscricaoProgramaService
from app.modules.society.juventude.domain.enums import StatusInscricao
router = APIRouter(prefix='/inscricoes-programa', tags=['Juventude - Inscricoes Programa'])

@router.post('/', response_model=InscricaoProgramaResponse, status_code=status.HTTP_201_CREATED)
async def inscrever_jovem(data: InscricaoProgramaCreate, service: InscricaoProgramaService=Depends(get_inscricao_programa_service)) -> InscricaoProgramaResponse:
    try:
        return await service.inscrever_jovem(programa_id=data.programa_id, jovem_id=data.jovem_id, prioridade=data.prioridade, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{inscricao_id}', response_model=InscricaoProgramaResponse)
async def obter_inscricao(inscricao_id: UUID, service: InscricaoProgramaService=Depends(get_inscricao_programa_service)) -> InscricaoProgramaResponse:
    try:
        return await service.buscar_inscricao(inscricao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[InscricaoProgramaResponse])
async def listar_inscricoes(jovem_id: UUID | None=None, programa_id: UUID | None=None, status_filtro: StatusInscricao | None=None, service: InscricaoProgramaService=Depends(get_inscricao_programa_service)) -> list[InscricaoProgramaResponse]:
    return await service.listar_inscricoes(jovem_id=jovem_id, programa_id=programa_id, status=status_filtro)

@router.patch('/{inscricao_id}/confirmar', response_model=InscricaoProgramaResponse)
async def confirmar_inscricao(inscricao_id: UUID, service: InscricaoProgramaService=Depends(get_inscricao_programa_service)) -> InscricaoProgramaResponse:
    try:
        return await service.confirmar_inscricao(inscricao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{inscricao_id}/concluir', response_model=InscricaoProgramaResponse)
async def concluir_inscricao(inscricao_id: UUID, service: InscricaoProgramaService=Depends(get_inscricao_programa_service)) -> InscricaoProgramaResponse:
    try:
        return await service.concluir_inscricao(inscricao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{inscricao_id}/cancelar', response_model=InscricaoProgramaResponse)
async def cancelar_inscricao(inscricao_id: UUID, data: InscricaoProgramaCancelar, service: InscricaoProgramaService=Depends(get_inscricao_programa_service)) -> InscricaoProgramaResponse:
    try:
        return await service.cancelar_inscricao(inscricao_id, data.motivo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.delete('/{inscricao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_inscricao(inscricao_id: UUID, service: InscricaoProgramaService=Depends(get_inscricao_programa_service)) -> None:
    try:
        await service.remover_inscricao(inscricao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))