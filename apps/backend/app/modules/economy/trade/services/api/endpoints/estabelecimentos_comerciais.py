from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.economy.trade.services.api.deps import get_estabelecimento_comercial_service
from app.modules.economy.trade.services.api.schemas.estabelecimento_comercial_schema import DataInput, EncerramentoInput, EstabelecimentoComercialCreate, EstabelecimentoComercialResponse, MotivoInput, PorteInput, RamoInput
from app.modules.economy.trade.services.application.services import EstabelecimentoComercialService
from app.modules.economy.trade.services.domain.enums import RamoComercial, StatusComercial
from app.modules.economy.trade.services.exceptions import EstabelecimentoComercialAlreadyExistsError, EstabelecimentoComercialNotFoundError, InvalidEstabelecimentoComercialStateError
router = APIRouter(prefix='/estabelecimentos_comerciais', tags=['Comercio Servicos - Estabelecimentos Comerciais'])

@router.post('/', response_model=EstabelecimentoComercialResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_estabelecimento_comercial(data: EstabelecimentoComercialCreate, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    try:
        return await service.cadastrar(cnpj=data.cnpj, razao_social=data.razao_social, tipo=data.tipo, ramo=data.ramo, porte=data.porte, regime_tributario=data.regime_tributario, cnae_principal=data.cnae_principal, data_abertura=data.data_abertura, endereco=data.endereco, numero=data.numero, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, cep=data.cep)
    except EstabelecimentoComercialAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/iniciar_atividades', response_model=EstabelecimentoComercialResponse)
async def iniciar_atividades(item_id: UUID, data: DataInput, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    try:
        return await service.iniciar_atividades(item_id, data_inicio=data.data)
    except EstabelecimentoComercialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidEstabelecimentoComercialStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/suspender_atividades', response_model=EstabelecimentoComercialResponse)
async def suspender_atividades(item_id: UUID, data: MotivoInput, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    try:
        return await service.suspender_atividades(item_id, motivo=data.motivo)
    except EstabelecimentoComercialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidEstabelecimentoComercialStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/encerrar', response_model=EstabelecimentoComercialResponse)
async def encerrar(item_id: UUID, data: EncerramentoInput, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    try:
        return await service.encerrar(item_id, data_encerramento=data.data_encerramento, motivo=data.motivo)
    except EstabelecimentoComercialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidEstabelecimentoComercialStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/associar_ramo', response_model=EstabelecimentoComercialResponse)
async def associar_ramo(item_id: UUID, data: RamoInput, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    try:
        return await service.associar_ramo(item_id, ramo=data.ramo)
    except EstabelecimentoComercialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{item_id}/definir_porte', response_model=EstabelecimentoComercialResponse)
async def definir_porte(item_id: UUID, data: PorteInput, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    try:
        return await service.definir_porte(item_id, porte=data.porte)
    except EstabelecimentoComercialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/{item_id}', response_model=EstabelecimentoComercialResponse)
async def obter_por_id(item_id: UUID, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    try:
        return await service.obter_por_id(item_id)
    except EstabelecimentoComercialNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EstabelecimentoComercialResponse])
async def listar(status_comercial: StatusComercial | None=None, ramo: RamoComercial | None=None, municipio: str | None=None, service: EstabelecimentoComercialService=Depends(get_estabelecimento_comercial_service)):
    return await service.listar(status=status_comercial, ramo=ramo, municipio=municipio)