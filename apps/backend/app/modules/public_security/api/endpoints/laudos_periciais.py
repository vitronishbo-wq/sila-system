from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.public_security.api.deps import get_laudo_pericial_service
from apps.backend.app.modules.public_security.api.schemas.laudo_pericial_schema import LaudoPericialCreate, LaudoPericialResponse, LaudoPericialStatusUpdate
from apps.backend.app.modules.public_security.application.services.laudo_pericial_service import LaudoPericialService
from apps.backend.app.modules.public_security.domain.enums import StatusLaudo, TipoLaudo
router = APIRouter(prefix='/laudos-periciais', tags=['Seguranca Publica - Laudos Periciais'])

@router.post('/', response_model=LaudoPericialResponse, status_code=status.HTTP_201_CREATED)
async def emitir_laudo_pericial(data: LaudoPericialCreate, service: LaudoPericialService=Depends(get_laudo_pericial_service)) -> LaudoPericialResponse:
    try:
        return await service.emitir_laudo(prova_id=data.prova_id, tipo_laudo=data.tipo_laudo, perito_id=data.perito_id, conclusao=data.conclusao, resumo=data.resumo, arquivo_url=data.arquivo_url, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{laudo_id}', response_model=LaudoPericialResponse)
async def obter_laudo_pericial(laudo_id: UUID, service: LaudoPericialService=Depends(get_laudo_pericial_service)) -> LaudoPericialResponse:
    try:
        return await service.buscar_laudo(laudo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[LaudoPericialResponse])
async def listar_laudos_periciais(prova_id: UUID | None=None, tipo: TipoLaudo | None=None, status_laudo: StatusLaudo | None=None, service: LaudoPericialService=Depends(get_laudo_pericial_service)) -> list[LaudoPericialResponse]:
    return await service.listar_laudos(prova_id=prova_id, tipo=tipo, status=status_laudo)

@router.patch('/{laudo_id}/status', response_model=LaudoPericialResponse)
async def atualizar_status_laudo(laudo_id: UUID, data: LaudoPericialStatusUpdate, service: LaudoPericialService=Depends(get_laudo_pericial_service)) -> LaudoPericialResponse:
    try:
        return await service.atualizar_status(laudo_id=laudo_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{laudo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_laudo_pericial(laudo_id: UUID, service: LaudoPericialService=Depends(get_laudo_pericial_service)) -> None:
    try:
        await service.remover_laudo(laudo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))