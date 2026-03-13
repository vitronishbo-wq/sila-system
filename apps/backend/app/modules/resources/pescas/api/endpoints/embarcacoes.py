from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.modules.resources.pescas.api.deps import get_embarcacao_service
from app.modules.resources.pescas.api.schemas.embarcacao_schema import EmbarcacaoCreate, EmbarcacaoResponse
from app.modules.resources.pescas.application.services.embarcacao_service import EmbarcacaoService
router = APIRouter(prefix='/embarcacoes', tags=['Pescas - Embarcacoes'])

@router.post('/', response_model=EmbarcacaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_embarcacao(data: EmbarcacaoCreate, service: EmbarcacaoService=Depends(get_embarcacao_service)):
    try:
        return await service.cadastrar_embarcacao(nome=data.nome, tipo=data.tipo, comprimento=data.comprimento, arqueacao_bruta=data.arqueacao_bruta, porto_registro=data.porto_registro, proprietario_id=data.proprietario_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{embarcacao_id}', response_model=EmbarcacaoResponse)
async def obter_embarcacao(embarcacao_id: UUID, service: EmbarcacaoService=Depends(get_embarcacao_service)):
    try:
        return await service.buscar_embarcacao(embarcacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EmbarcacaoResponse])
async def listar_embarcacoes(proprietario_id: UUID=Query(...), service: EmbarcacaoService=Depends(get_embarcacao_service)):
    return await service.listar_embarcacoes(proprietario_id=proprietario_id)