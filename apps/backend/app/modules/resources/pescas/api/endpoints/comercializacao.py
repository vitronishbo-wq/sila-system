from __future__ import annotations
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from app.modules.resources.pescas.api.deps import get_comercializacao_service
from app.modules.resources.pescas.application.services.comercializacao_service import ComercializacaoService
router = APIRouter(prefix='/comercializacao', tags=['Pescas - Comercializacao'])

class ComercializacaoCreate(BaseModel):
    produto: str
    quantidade_kg: Decimal
    preco_unitario: Decimal
    data_operacao: date
    comprador: str

class ComercializacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    produto: str
    quantidade_kg: Decimal
    preco_unitario: Decimal
    data_operacao: date
    comprador: str
    observacoes: Optional[str] = None

@router.post('/', response_model=ComercializacaoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_comercializacao(data: ComercializacaoCreate, service: ComercializacaoService=Depends(get_comercializacao_service)):
    return await service.registrar_operacao(produto=data.produto, quantidade_kg=data.quantidade_kg, preco_unitario=data.preco_unitario, data_operacao=data.data_operacao, comprador=data.comprador)

@router.get('/', response_model=list[ComercializacaoResponse])
async def listar_comercializacao(service: ComercializacaoService=Depends(get_comercializacao_service)):
    return await service.listar()