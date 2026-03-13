from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.society.cultura.api.deps import get_patrimonio_imaterial_service
from app.modules.society.cultura.api.schemas.patrimonio_imaterial_schema import PatrimonioImaterialCreate, PatrimonioImaterialResponse, PatrimonioImaterialUpdate
from app.modules.society.cultura.application.services.patrimonio_imaterial_service import PatrimonioImaterialService
from app.modules.society.cultura.domain.enums import CategoriaPatrimonioImaterial, StatusPatrimonioImaterial
router = APIRouter(prefix='/patrimonios-imateriais', tags=['Cultura - Patrimonios Imateriais'])

@router.post('/', response_model=PatrimonioImaterialResponse, status_code=status.HTTP_201_CREATED)
async def registrar_patrimonio(data: PatrimonioImaterialCreate, service: PatrimonioImaterialService=Depends(get_patrimonio_imaterial_service)) -> PatrimonioImaterialResponse:
    try:
        return await service.registrar_patrimonio(nome=data.nome, categoria=data.categoria, descricao=data.descricao, comunidade=data.comunidade, municipio=data.municipio, provincia=data.provincia, atracao_turistica_id=data.atracao_turistica_id, instituicao_educacional_id=data.instituicao_educacional_id, plano_salvaguarda=data.plano_salvaguarda, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{patrimonio_id}', response_model=PatrimonioImaterialResponse)
async def obter_patrimonio(patrimonio_id: UUID, service: PatrimonioImaterialService=Depends(get_patrimonio_imaterial_service)) -> PatrimonioImaterialResponse:
    try:
        return await service.buscar_patrimonio(patrimonio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[PatrimonioImaterialResponse])
async def listar_patrimonios(categoria: CategoriaPatrimonioImaterial | None=None, municipio: str | None=None, status_registro: StatusPatrimonioImaterial | None=None, somente_ativos: bool=True, service: PatrimonioImaterialService=Depends(get_patrimonio_imaterial_service)) -> list[PatrimonioImaterialResponse]:
    return await service.listar_patrimonios(categoria=categoria, municipio=municipio, status=status_registro, somente_ativos=somente_ativos)

@router.patch('/{patrimonio_id}', response_model=PatrimonioImaterialResponse)
async def atualizar_patrimonio(patrimonio_id: UUID, data: PatrimonioImaterialUpdate, service: PatrimonioImaterialService=Depends(get_patrimonio_imaterial_service)) -> PatrimonioImaterialResponse:
    try:
        return await service.atualizar_patrimonio(patrimonio_id=patrimonio_id, nome=data.nome, categoria=data.categoria, descricao=data.descricao, comunidade=data.comunidade, municipio=data.municipio, provincia=data.provincia, atracao_turistica_id=data.atracao_turistica_id, instituicao_educacional_id=data.instituicao_educacional_id, plano_salvaguarda=data.plano_salvaguarda, status=data.status, ativo=data.ativo, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.delete('/{patrimonio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_patrimonio(patrimonio_id: UUID, service: PatrimonioImaterialService=Depends(get_patrimonio_imaterial_service)) -> None:
    try:
        await service.remover_patrimonio(patrimonio_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))