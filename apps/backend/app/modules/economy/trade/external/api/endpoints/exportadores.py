from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.economy.trade.external.api.deps import get_exportador_service
from app.modules.economy.trade.external.api.schemas.exportador_schema import CancelamentoInput, ExportadorCreate, ExportadorResponse, HabilitacaoInput, PaisDestinoInput, ProdutoInput, SuspensaoInput
from app.modules.economy.trade.external.application.services import ExportadorService
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao
from app.modules.economy.trade.external.exceptions import ExportadorAlreadyExistsError, ExportadorNotFoundError, InvalidExportadorStateError
router = APIRouter(prefix='/exportadores', tags=['Comercio Externo - Exportadores'])

@router.post('/', response_model=ExportadorResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_exportador(data: ExportadorCreate, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.cadastrar(razao_social=data.razao_social, cnpj_cpf=data.cnpj_cpf, tipo_pessoa=data.tipo_pessoa, endereco=data.endereco, numero=data.numero, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, cep=data.cep, regimes_autorizados=data.regimes_autorizados)
    except ExportadorAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/habilitar', response_model=ExportadorResponse)
async def habilitar_exportador(item_id: UUID, data: HabilitacaoInput, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.habilitar(item_id, numero_radar=data.numero_radar, data_habilitacao=data.data_habilitacao, data_validade=data.data_validade)
    except ExportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidExportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/suspender', response_model=ExportadorResponse)
async def suspender_exportador(item_id: UUID, data: SuspensaoInput, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.suspender(item_id, data_suspensao=data.data_suspensao, motivo=data.motivo)
    except ExportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidExportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/cancelar', response_model=ExportadorResponse)
async def cancelar_exportador(item_id: UUID, data: CancelamentoInput, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.cancelar(item_id, data_cancelamento=data.data_cancelamento, motivo=data.motivo)
    except ExportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidExportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/reabilitar', response_model=ExportadorResponse)
async def reabilitar_exportador(item_id: UUID, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.reabilitar(item_id)
    except ExportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidExportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/produtos', response_model=ExportadorResponse)
async def adicionar_produto(item_id: UUID, data: ProdutoInput, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.adicionar_produto(item_id, produto=data.produto)
    except ExportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidExportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{item_id}/paises-destino', response_model=ExportadorResponse)
async def adicionar_pais_destino(item_id: UUID, data: PaisDestinoInput, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.adicionar_pais_destino(item_id, pais=data.pais)
    except ExportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidExportadorStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{item_id}', response_model=ExportadorResponse)
async def obter_exportador(item_id: UUID, service: ExportadorService=Depends(get_exportador_service)):
    try:
        return await service.obter_por_id(item_id)
    except ExportadorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ExportadorResponse])
async def listar_exportadores(status_habilitacao: StatusHabilitacao | None=None, municipio: str | None=None, service: ExportadorService=Depends(get_exportador_service)):
    return await service.listar(status=status_habilitacao, municipio=municipio)