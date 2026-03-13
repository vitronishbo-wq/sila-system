from __future__ import annotations
from fastapi import APIRouter, Depends, status
from apps.backend.app.modules.resources.pescas.api.deps import get_producao_service
from apps.backend.app.modules.resources.pescas.api.schemas.producao_schema import ProducaoCreate, ProducaoResponse
from apps.backend.app.modules.resources.pescas.application.services.producao_pesca_service import ProducaoPescaService
router = APIRouter(prefix='/producao', tags=['Pescas - Producao'])

@router.post('/', response_model=ProducaoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_producao(data: ProducaoCreate, service: ProducaoPescaService=Depends(get_producao_service)):
    return await service.registrar_producao(data_producao=data.data_producao, quantidade_kg=data.quantidade_kg, unidade_processamento=data.unidade_processamento, destino=data.destino)

@router.get('/', response_model=list[ProducaoResponse])
async def listar_producao(service: ProducaoPescaService=Depends(get_producao_service)):
    return await service.listar()