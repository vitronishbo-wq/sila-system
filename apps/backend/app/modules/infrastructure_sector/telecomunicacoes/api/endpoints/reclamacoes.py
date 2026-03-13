from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_reclamacao_service
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.reclamacao_schema import ReclamacaoCreate, ReclamacaoResponse
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.reclamacao_service import ReclamacaoService
router = APIRouter(prefix='/reclamacoes', tags=['Telecomunicacoes - Reclamacoes'])

@router.post('/', response_model=ReclamacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_reclamacao(payload: ReclamacaoCreate, service: ReclamacaoService=Depends(get_reclamacao_service)) -> ReclamacaoResponse:
    try:
        return await service.criar_reclamacao(assinante_id=payload.assinante_id, tipo=payload.tipo, descricao=payload.descricao, prioridade=payload.prioridade)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/assinante/{assinante_id}', response_model=list[ReclamacaoResponse])
async def listar_reclamacoes_assinante(assinante_id: UUID, service: ReclamacaoService=Depends(get_reclamacao_service)) -> list[ReclamacaoResponse]:
    return await service.listar_reclamacoes_assinante(assinante_id)