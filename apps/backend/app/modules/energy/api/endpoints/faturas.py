from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.energy.api.deps import get_faturamento_service
from apps.backend.app.modules.energy.api.schemas.fatura_schema import FaturaEnergiaResponse, FaturaGerarPorConsumoInput, FaturaPagamentoInput
from apps.backend.app.modules.energy.application.services import FaturamentoService
from apps.backend.app.modules.energy.domain.enums import StatusFaturaEnergia
from apps.backend.app.modules.energy.domain.exceptions import ConsumoNotFoundError, FaturaEnergiaAlreadyExistsError, FaturaEnergiaNotFoundError
router = APIRouter(prefix='/faturas', tags=['Energia - Faturas'])

@router.post('/gerar-por-consumo', response_model=FaturaEnergiaResponse, status_code=status.HTTP_201_CREATED)
async def gerar_por_consumo(data: FaturaGerarPorConsumoInput, service: FaturamentoService=Depends(get_faturamento_service)):
    try:
        return await service.gerar_fatura_por_consumo(data.consumo_id, data_referencia=data.data_referencia)
    except ConsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except FaturaEnergiaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_fatura}/pagamento', response_model=FaturaEnergiaResponse)
async def registrar_pagamento(numero_fatura: str, data: FaturaPagamentoInput, service: FaturamentoService=Depends(get_faturamento_service)):
    try:
        return await service.registrar_pagamento(numero_fatura, data_pagamento=data.data_pagamento, valor_pago=data.valor_pago, metodo_pagamento=data.metodo_pagamento)
    except FaturaEnergiaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_fatura}', response_model=FaturaEnergiaResponse)
async def obter_fatura(numero_fatura: str, service: FaturamentoService=Depends(get_faturamento_service)):
    try:
        return await service.obter_por_numero(numero_fatura)
    except FaturaEnergiaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[FaturaEnergiaResponse])
async def listar_faturas(unidade_consumidora_id: UUID | None=None, cpf_titular: str | None=None, status_fatura: StatusFaturaEnergia | None=None, service: FaturamentoService=Depends(get_faturamento_service)):
    return await service.listar(unidade_consumidora_id=unidade_consumidora_id, cpf_titular=cpf_titular, status=status_fatura)
