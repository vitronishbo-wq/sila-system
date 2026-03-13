from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.logistics.api.deps import get_bilhetagem_service
from apps.backend.app.modules.logistics.api.schemas.bilhetagem_schema import BilhetagemEventoCreate, BilhetagemEventoResponse, BilhetagemReconciliacaoInput
from apps.backend.app.modules.logistics.application.services import BilhetagemService
from apps.backend.app.modules.logistics.domain.enums import StatusReconciliacaoFinanceira
from apps.backend.app.modules.logistics.domain.exceptions import BilhetagemNotFoundError
router = APIRouter(prefix='/bilhetagem', tags=['Transportes Logistica - Bilhetagem'])

def _has_capability(service: BilhetagemService, method_name: str) -> bool:
    checker = getattr(service, method_name, None)
    if checker is None:
        return True
    return bool(checker())

def _ensure_financas_adapter(service: BilhetagemService) -> None:
    if not _has_capability(service, 'has_financas_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Financas indisponivel para bilhetagem reconciliavel.')

@router.post('/eventos', response_model=BilhetagemEventoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_evento(data: BilhetagemEventoCreate, service: BilhetagemService=Depends(get_bilhetagem_service)):
    _ensure_financas_adapter(service)
    try:
        return await service.registrar_evento(codigo_bilhete=data.codigo_bilhete, viagem_id=data.viagem_id, tipo_tarifa=data.tipo_tarifa, valor_pago=data.valor_pago, forma_pagamento=data.forma_pagamento, metadata=data.metadata)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/eventos/{evento_id}/reconciliar', response_model=BilhetagemEventoResponse)
async def reconciliar_evento(evento_id: UUID, data: BilhetagemReconciliacaoInput, service: BilhetagemService=Depends(get_bilhetagem_service)):
    _ensure_financas_adapter(service)
    try:
        return await service.reconciliar_evento(evento_id, confirmado=data.confirmado, referencia_externa=data.referencia_externa)
    except BilhetagemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/eventos/{evento_id}', response_model=BilhetagemEventoResponse)
async def obter_evento(evento_id: UUID, service: BilhetagemService=Depends(get_bilhetagem_service)):
    try:
        return await service.obter_evento(evento_id)
    except BilhetagemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/eventos', response_model=list[BilhetagemEventoResponse])
async def listar_eventos(viagem_id: UUID | None=None, codigo_bilhete: str | None=None, status_reconciliacao: StatusReconciliacaoFinanceira | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None, service: BilhetagemService=Depends(get_bilhetagem_service)):
    return await service.listar_eventos(viagem_id=viagem_id, codigo_bilhete=codigo_bilhete, status_reconciliacao=status_reconciliacao, data_inicio=data_inicio, data_fim=data_fim)
