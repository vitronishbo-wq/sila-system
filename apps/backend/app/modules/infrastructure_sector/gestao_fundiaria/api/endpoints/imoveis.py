from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_imovel_service
from app.modules.infrastructure_sector.gestao_fundiaria.api.schemas.imovel_schema import ImovelAreaInput, ImovelCreate, ImovelMatriculaInput, ImovelMotivoInput, ImovelProprietarioInput, ImovelResponse, ImovelSituacaoInput
from app.modules.infrastructure_sector.gestao_fundiaria.application.services.imovel_service import ImovelService
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ImovelAlreadyExistsError, ImovelNotFoundError
router = APIRouter(prefix='/imoveis', tags=['Gestao Fundiaria - Imoveis'])

@router.post('/', response_model=ImovelResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_imovel(data: ImovelCreate, service: ImovelService=Depends(get_imovel_service)):
    try:
        return await service.cadastrar(tipo=data.tipo, natureza=data.natureza, area_total=data.area_total, endereco=data.endereco, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, inscricao_imobiliaria=data.inscricao_imobiliaria)
    except ImovelAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{inscricao_imobiliaria:path}/area', response_model=ImovelResponse)
async def atualizar_area_imovel(inscricao_imobiliaria: str, data: ImovelAreaInput, service: ImovelService=Depends(get_imovel_service)):
    try:
        return await service.atualizar_area(inscricao_imobiliaria, area_total=data.area_total)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{inscricao_imobiliaria:path}/proprietario', response_model=ImovelResponse)
async def atualizar_proprietario_imovel(inscricao_imobiliaria: str, data: ImovelProprietarioInput, service: ImovelService=Depends(get_imovel_service)):
    try:
        return await service.atualizar_proprietario(inscricao_imobiliaria, proprietario_id=data.proprietario_id)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/{inscricao_imobiliaria:path}/situacao', response_model=ImovelResponse)
async def atualizar_situacao_imovel(inscricao_imobiliaria: str, data: ImovelSituacaoInput, service: ImovelService=Depends(get_imovel_service)):
    try:
        return await service.atualizar_situacao(inscricao_imobiliaria, situacao=data.situacao)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/{inscricao_imobiliaria:path}/matricula', response_model=ImovelResponse)
async def vincular_matricula_imovel(inscricao_imobiliaria: str, data: ImovelMatriculaInput, service: ImovelService=Depends(get_imovel_service)):
    try:
        return await service.vincular_matricula(inscricao_imobiliaria, matricula_id=data.matricula_id)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/{inscricao_imobiliaria:path}/desativar', response_model=ImovelResponse)
async def desativar_imovel(inscricao_imobiliaria: str, data: ImovelMotivoInput, service: ImovelService=Depends(get_imovel_service)):
    try:
        return await service.desativar(inscricao_imobiliaria, motivo=data.motivo)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{inscricao_imobiliaria:path}', response_model=ImovelResponse)
async def obter_imovel(inscricao_imobiliaria: str, service: ImovelService=Depends(get_imovel_service)):
    try:
        return await service.obter_por_inscricao(inscricao_imobiliaria)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ImovelResponse])
async def listar_imoveis(proprietario_atual_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None, ativo: bool | None=None, service: ImovelService=Depends(get_imovel_service)):
    return await service.listar(proprietario_atual_id=proprietario_atual_id, municipio=municipio, provincia=provincia, ativo=ativo)