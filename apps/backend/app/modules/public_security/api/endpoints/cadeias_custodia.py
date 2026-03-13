from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.public_security.api.deps import get_cadeia_custodia_service
from app.modules.public_security.api.schemas.cadeia_custodia_schema import CadeiaCustodiaCreate, CadeiaCustodiaMovimentacao, CadeiaCustodiaResponse
from app.modules.public_security.application.services.cadeia_custodia_service import CadeiaCustodiaService
from app.modules.public_security.domain.enums import StatusCadeiaCustodia
router = APIRouter(prefix='/cadeias-custodia', tags=['Seguranca Publica - Cadeia Custodia'])

@router.post('/', response_model=CadeiaCustodiaResponse, status_code=status.HTTP_201_CREATED)
async def iniciar_cadeia_custodia(data: CadeiaCustodiaCreate, service: CadeiaCustodiaService=Depends(get_cadeia_custodia_service)) -> CadeiaCustodiaResponse:
    try:
        return await service.iniciar_cadeia(prova_id=data.prova_id, local_atual=data.local_atual, responsavel_id=data.responsavel_id, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{cadeia_id}', response_model=CadeiaCustodiaResponse)
async def obter_cadeia_custodia(cadeia_id: UUID, service: CadeiaCustodiaService=Depends(get_cadeia_custodia_service)) -> CadeiaCustodiaResponse:
    try:
        return await service.buscar_cadeia(cadeia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[CadeiaCustodiaResponse])
async def listar_cadeias_custodia(status_cadeia: StatusCadeiaCustodia | None=None, service: CadeiaCustodiaService=Depends(get_cadeia_custodia_service)) -> list[CadeiaCustodiaResponse]:
    return await service.listar_cadeias(status=status_cadeia)

@router.patch('/{cadeia_id}/movimentacoes', response_model=CadeiaCustodiaResponse)
async def registrar_movimentacao_cadeia(cadeia_id: UUID, data: CadeiaCustodiaMovimentacao, service: CadeiaCustodiaService=Depends(get_cadeia_custodia_service)) -> CadeiaCustodiaResponse:
    try:
        return await service.registrar_movimentacao(cadeia_id=cadeia_id, status=data.status, local_atual=data.local_atual, responsavel_id=data.responsavel_id, observacao=data.observacao)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{cadeia_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_cadeia_custodia(cadeia_id: UUID, service: CadeiaCustodiaService=Depends(get_cadeia_custodia_service)) -> None:
    try:
        await service.remover_cadeia(cadeia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))