from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.cultura.api.deps import get_espaco_cultural_service
from apps.backend.app.modules.society.cultura.api.schemas.espaco_cultural_schema import EspacoCulturalCreate, EspacoCulturalResponse, EspacoCulturalUpdate
from apps.backend.app.modules.society.cultura.application.services.espaco_cultural_service import EspacoCulturalService
from apps.backend.app.modules.society.cultura.domain.enums import TipoEspacoCultural
router = APIRouter(prefix='/espacos-culturais', tags=['Cultura - Espacos Culturais'])

@router.post('/', response_model=EspacoCulturalResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_espaco(data: EspacoCulturalCreate, service: EspacoCulturalService=Depends(get_espaco_cultural_service)) -> EspacoCulturalResponse:
    try:
        return await service.cadastrar_espaco(nome=data.nome, tipo=data.tipo, municipio=data.municipio, provincia=data.provincia, endereco=data.endereco, capacidade=data.capacidade, area_m2=data.area_m2, administracao=data.administracao, responsavel_cpf=data.responsavel_cpf, orgao_gestor=data.orgao_gestor, ano_inauguracao=data.ano_inauguracao, acessibilidade=data.acessibilidade, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{espaco_id}', response_model=EspacoCulturalResponse)
async def obter_espaco(espaco_id: UUID, service: EspacoCulturalService=Depends(get_espaco_cultural_service)) -> EspacoCulturalResponse:
    try:
        return await service.buscar_espaco(espaco_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EspacoCulturalResponse])
async def listar_espacos(tipo: TipoEspacoCultural | None=None, municipio: str | None=None, somente_ativos: bool=True, service: EspacoCulturalService=Depends(get_espaco_cultural_service)) -> list[EspacoCulturalResponse]:
    return await service.listar_espacos(tipo=tipo, municipio=municipio, somente_ativos=somente_ativos)

@router.patch('/{espaco_id}', response_model=EspacoCulturalResponse)
async def atualizar_espaco(espaco_id: UUID, data: EspacoCulturalUpdate, service: EspacoCulturalService=Depends(get_espaco_cultural_service)) -> EspacoCulturalResponse:
    try:
        return await service.atualizar_espaco(espaco_id=espaco_id, nome=data.nome, tipo=data.tipo, municipio=data.municipio, provincia=data.provincia, endereco=data.endereco, capacidade=data.capacidade, area_m2=data.area_m2, administracao=data.administracao, responsavel_cpf=data.responsavel_cpf, orgao_gestor=data.orgao_gestor, ano_inauguracao=data.ano_inauguracao, acessibilidade=data.acessibilidade, ativo=data.ativo, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.delete('/{espaco_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_espaco(espaco_id: UUID, service: EspacoCulturalService=Depends(get_espaco_cultural_service)) -> None:
    try:
        await service.remover_espaco(espaco_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))