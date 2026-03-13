from __future__ import annotations
from fastapi import APIRouter, Depends, status
from apps.backend.app.modules.resources.pescas.api.deps import get_fiscalizacao_service
from apps.backend.app.modules.resources.pescas.api.schemas.fiscalizacao_schema import FiscalizacaoCreate, FiscalizacaoResponse
from apps.backend.app.modules.resources.pescas.application.services.fiscalizacao_service import FiscalizacaoService
router = APIRouter(prefix='/fiscalizacao', tags=['Pescas - Fiscalizacao'])

@router.post('/', response_model=FiscalizacaoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_fiscalizacao(data: FiscalizacaoCreate, service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    return await service.registrar_fiscalizacao(embarcacao_id=data.embarcacao_id, local=data.local, agente=data.agente, regular=data.regular, observacoes=data.observacoes)

@router.get('/', response_model=list[FiscalizacaoResponse])
async def listar_fiscalizacoes(service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    return await service.listar()