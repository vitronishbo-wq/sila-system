from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_faturamento_service
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.fatura_schema import FaturaGerarInput, FaturaTelecomResponse
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.faturamento_service import FaturamentoService
router = APIRouter(prefix='/faturas', tags=['Telecomunicacoes - Faturas'])

@router.post('/{assinante_id}', response_model=FaturaTelecomResponse, status_code=status.HTTP_201_CREATED)
async def gerar_fatura(assinante_id: UUID, data: FaturaGerarInput, service: FaturamentoService=Depends(get_faturamento_service)) -> FaturaTelecomResponse:
    try:
        return await service.gerar_fatura_mensal(assinante_id, data.referencia, consumo_total_gb=data.consumo_total_gb)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/assinante/{assinante_id}', response_model=list[FaturaTelecomResponse])
async def listar_faturas_assinante(assinante_id: UUID, service: FaturamentoService=Depends(get_faturamento_service)) -> list[FaturaTelecomResponse]:
    return await service.listar_faturas_assinante(assinante_id)