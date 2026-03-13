from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.economy.trade.external.api.deps import get_importador_service
from app.modules.economy.trade.external.api.schemas.importador_schema import CancelamentoImportadorInput, HabilitacaoImportadorInput, ImportadorCreate, ImportadorResponse, PaisOrigemInput, ProdutoImportadorInput, SuspensaoImportadorInput
from app.modules.economy.trade.external.application.services import ImportadorService
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao
from app.modules.economy.trade.external.exceptions import ImportadorAlreadyExistsError, ImportadorNotFoundError, InvalidImportadorStateError
router = APIRouter(prefix='/importadores', tags=['Comercio Externo - Importadores'])

@router.post('/', response_model=ImportadorResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_importador(data: ImportadorCreate, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.cadastrar(razao_social=data.razao_social, cnpj_cpf=data.cnpj_cpf, tipo_pessoa=data.tipo_pessoa, endereco=data.endereco, numero=data.numero, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, cep=data.cep, regimes_autorizados=data.regimes_autorizados)
    except ImportadorAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/habilitar', response_model=ImportadorResponse)
async def habilitar_importador(item_id: UUID, data: HabilitacaoImportadorInput, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.habilitar(item_id, numero_radar=data.numero_radar, data_habilitacao=data.data_habilitacao, data_validade=data.data_validade)
    except ImportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidImportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/suspender', response_model=ImportadorResponse)
async def suspender_importador(item_id: UUID, data: SuspensaoImportadorInput, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.suspender(item_id, data_suspensao=data.data_suspensao, motivo=data.motivo)
    except ImportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidImportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/cancelar', response_model=ImportadorResponse)
async def cancelar_importador(item_id: UUID, data: CancelamentoImportadorInput, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.cancelar(item_id, data_cancelamento=data.data_cancelamento, motivo=data.motivo)
    except ImportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidImportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/reabilitar', response_model=ImportadorResponse)
async def reabilitar_importador(item_id: UUID, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.reabilitar(item_id)
    except ImportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidImportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/produtos', response_model=ImportadorResponse)
async def adicionar_produto_importador(item_id: UUID, data: ProdutoImportadorInput, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.adicionar_produto(item_id, produto=data.produto)
    except ImportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidImportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/paises-origem', response_model=ImportadorResponse)
async def adicionar_pais_origem(item_id: UUID, data: PaisOrigemInput, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.adicionar_pais_origem(item_id, pais=data.pais)
    except ImportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidImportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{item_id}', response_model=ImportadorResponse)
async def obter_importador(item_id: UUID, service: ImportadorService=Depends(get_importador_service)):
    try:
        return await service.obter_por_id(item_id)
    except ImportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ImportadorResponse])
async def listar_importadores(status_habilitacao: StatusHabilitacao | None=None, municipio: str | None=None, service: ImportadorService=Depends(get_importador_service)):
    return await service.listar(status=status_habilitacao, municipio=municipio)