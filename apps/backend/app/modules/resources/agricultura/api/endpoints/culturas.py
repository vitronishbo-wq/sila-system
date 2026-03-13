from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.agricultura.api.deps import get_producao_service
from app.modules.resources.agricultura.api.schemas.cultura_schema import CulturaCreate, CulturaResponse
from app.modules.resources.agricultura.application.services.producao_service import ProducaoService
from app.modules.resources.agricultura.exceptions import CulturaNotFoundError
router = APIRouter(prefix='/culturas', tags=['Agricultura - culturas'])

@router.post('/', response_model=CulturaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_cultura(data: CulturaCreate, service: ProducaoService=Depends(get_producao_service)):
    try:
        return await service.cadastrar_cultura(nome=data.nome, tipo=data.tipo, ciclo_dias=data.ciclo_dias, produtividade_estimada_ton_ha=data.produtividade_estimada_ton_ha)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_cultura:path}', response_model=CulturaResponse)
async def obter_cultura(codigo_cultura: str, service: ProducaoService=Depends(get_producao_service)):
    try:
        return await service.obter_cultura(codigo_cultura)
    except CulturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[CulturaResponse])
async def listar_culturas(service: ProducaoService=Depends(get_producao_service)):
    return await service.listar_culturas()