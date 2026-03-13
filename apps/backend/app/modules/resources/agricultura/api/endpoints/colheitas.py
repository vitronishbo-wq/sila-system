from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.resources.agricultura.api.deps import get_colheita_service
from apps.backend.app.modules.resources.agricultura.api.schemas.colheita_schema import ColheitaCreate, ColheitaResponse
from apps.backend.app.modules.resources.agricultura.application.services.colheita_service import ColheitaService
from apps.backend.app.modules.resources.agricultura.exceptions import ColheitaNotFoundError, SafraNotFoundError, TalhaoNotFoundError
router = APIRouter(prefix='/colheitas', tags=['Agricultura - colheitas'])

@router.post('/', response_model=ColheitaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_colheita(data: ColheitaCreate, service: ColheitaService=Depends(get_colheita_service)):
    try:
        return await service.registrar(codigo_safra=data.codigo_safra, codigo_talhao=data.codigo_talhao, quantidade_colhida_ton=data.quantidade_colhida_ton, perdas_ton=data.perdas_ton, umidade_percentual=data.umidade_percentual, observacoes=data.observacoes)
    except (SafraNotFoundError, TalhaoNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_colheita:path}', response_model=ColheitaResponse)
async def obter_colheita(codigo_colheita: str, service: ColheitaService=Depends(get_colheita_service)):
    try:
        return await service.obter(codigo_colheita)
    except ColheitaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ColheitaResponse])
async def listar_colheitas(codigo_safra: str | None=None, codigo_talhao: str | None=None, service: ColheitaService=Depends(get_colheita_service)):
    return await service.listar(codigo_safra=codigo_safra, codigo_talhao=codigo_talhao)