from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.pescas.api.deps import get_especie_catalog_service
from app.modules.resources.pescas.api.schemas.especie_schema import EspecieCreate, EspecieResponse
router = APIRouter(prefix='/especies', tags=['Pescas - Especies'])

@router.post('/', response_model=EspecieResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_especie(data: EspecieCreate, service=Depends(get_especie_catalog_service)):
    return await service.cadastrar(nome_comum=data.nome_comum, nome_cientifico=data.nome_cientifico, codigo_fao=data.codigo_fao)

@router.get('/{especie_id}', response_model=EspecieResponse)
async def obter_especie(especie_id: UUID, service=Depends(get_especie_catalog_service)):
    item = await service.obter(especie_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Especie nao encontrada')
    return item

@router.get('/', response_model=list[EspecieResponse])
async def listar_especies(service=Depends(get_especie_catalog_service)):
    return await service.listar()