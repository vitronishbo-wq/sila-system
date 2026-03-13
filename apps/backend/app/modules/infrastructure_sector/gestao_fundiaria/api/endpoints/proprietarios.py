from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_proprietario_service
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.schemas.proprietario_schema import ProprietarioContatoInput, ProprietarioCreate, ProprietarioMotivoInput, ProprietarioResponse, ProprietarioTitularidadeInput
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.proprietario_service import ProprietarioService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ProprietarioAlreadyExistsError, ProprietarioNotFoundError
router = APIRouter(prefix='/proprietarios', tags=['Gestao Fundiaria - Proprietarios'])

@router.post('/', response_model=ProprietarioResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_proprietario(data: ProprietarioCreate, service: ProprietarioService=Depends(get_proprietario_service)):
    try:
        return await service.cadastrar(nome=data.nome, documento=data.documento, tipo_pessoa=data.tipo_pessoa, tipo_titularidade=data.tipo_titularidade, percentual_titularidade=data.percentual_titularidade, email=data.email, telefone=data.telefone, endereco=data.endereco)
    except ProprietarioAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_cadastro:path}/contato', response_model=ProprietarioResponse)
async def atualizar_contato_proprietario(numero_cadastro: str, data: ProprietarioContatoInput, service: ProprietarioService=Depends(get_proprietario_service)):
    try:
        return await service.atualizar_contato(numero_cadastro, email=data.email, telefone=data.telefone, endereco=data.endereco)
    except ProprietarioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/{numero_cadastro:path}/titularidade', response_model=ProprietarioResponse)
async def atualizar_titularidade_proprietario(numero_cadastro: str, data: ProprietarioTitularidadeInput, service: ProprietarioService=Depends(get_proprietario_service)):
    try:
        return await service.atualizar_titularidade(numero_cadastro, tipo_titularidade=data.tipo_titularidade, percentual_titularidade=data.percentual_titularidade)
    except ProprietarioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_cadastro:path}/desativar', response_model=ProprietarioResponse)
async def desativar_proprietario(numero_cadastro: str, data: ProprietarioMotivoInput, service: ProprietarioService=Depends(get_proprietario_service)):
    try:
        return await service.desativar(numero_cadastro, motivo=data.motivo)
    except ProprietarioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_cadastro:path}', response_model=ProprietarioResponse)
async def obter_proprietario(numero_cadastro: str, service: ProprietarioService=Depends(get_proprietario_service)):
    try:
        return await service.obter_por_numero_cadastro(numero_cadastro)
    except ProprietarioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ProprietarioResponse])
async def listar_proprietarios(tipo_pessoa: str | None=None, ativo: bool | None=None, service: ProprietarioService=Depends(get_proprietario_service)):
    return await service.listar(tipo_pessoa=tipo_pessoa, ativo=ativo)