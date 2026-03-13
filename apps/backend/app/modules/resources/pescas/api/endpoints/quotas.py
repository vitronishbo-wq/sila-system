from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from apps.backend.app.modules.resources.pescas.api.deps import get_quota_service
from apps.backend.app.modules.resources.pescas.api.schemas.quota_schema import QuotaCreate, QuotaResponse
from apps.backend.app.modules.resources.pescas.application.services.quota_service import QuotaService
router = APIRouter(prefix='/quotas', tags=['Pescas - Quotas'])

class QuotaConsumoInput(BaseModel):
    quantidade_kg: Decimal

@router.post('/', response_model=QuotaResponse, status_code=status.HTTP_201_CREATED)
async def criar_quota(data: QuotaCreate, service: QuotaService=Depends(get_quota_service)):
    return await service.criar_quota(especie_id=data.especie_id, zona_pesca_id=data.zona_pesca_id, limite_kg=data.limite_kg)

@router.post('/{quota_id}/consumo', response_model=QuotaResponse)
async def registrar_consumo(quota_id: UUID, data: QuotaConsumoInput, service: QuotaService=Depends(get_quota_service)):
    try:
        return await service.registrar_consumo(quota_id=quota_id, quantidade_kg=data.quantidade_kg)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[QuotaResponse])
async def listar_quotas(service: QuotaService=Depends(get_quota_service)):
    return await service.listar()