from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.energy.api.deps import get_consumo_service
from apps.backend.app.modules.energy.api.schemas.consumo_schema import ConsumoLeituraInput, ConsumoResponse
from apps.backend.app.modules.energy.application.services import ConsumoService
from apps.backend.app.modules.energy.domain.exceptions import ConsumoNotFoundError
router = APIRouter(prefix='/consumos', tags=['Energia - Consumo'])

@router.post('/', response_model=ConsumoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_leitura(data: ConsumoLeituraInput, service: ConsumoService=Depends(get_consumo_service)):
    try:
        return await service.registrar_leitura(unidade_consumidora_id=data.unidade_consumidora_id, leitura_kwh=data.leitura_kwh, data_leitura=data.data_leitura, tipo_leitura=data.tipo_leitura, classe_tarifaria=data.classe_tarifaria, cpf_titular=data.cpf_titular, medidor_id=data.medidor_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{consumo_id}', response_model=ConsumoResponse)
async def obter_consumo(consumo_id: UUID, service: ConsumoService=Depends(get_consumo_service)):
    try:
        return await service.obter_por_id(consumo_id)
    except ConsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ConsumoResponse])
async def listar_consumos(unidade_consumidora_id: UUID | None=None, cpf_titular: str | None=None, service: ConsumoService=Depends(get_consumo_service)):
    return await service.listar(unidade_consumidora_id=unidade_consumidora_id, cpf_titular=cpf_titular)