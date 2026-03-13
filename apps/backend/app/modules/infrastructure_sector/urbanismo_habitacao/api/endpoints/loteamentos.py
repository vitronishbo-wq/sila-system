from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_loteamento_service
from app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.loteamento_schema import LoteamentoConclusaoInput, LoteamentoCreate, LoteamentoImplantacaoInput, LoteamentoInicioInput, LoteamentoMotivoInput, LoteamentoResponse
from app.modules.infrastructure_sector.urbanismo_habitacao.application.services.loteamento_service import LoteamentoService
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLoteamento, TipoLoteamento
from app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import LoteamentoAlreadyExistsError, LoteamentoNotFoundError
router = APIRouter(prefix='/loteamentos', tags=['Urbanismo Habitacao - Loteamentos'])

def _ensure_loteamento_create_adapters(service: LoteamentoService) -> None:
    if not service.has_gestao_fundiaria_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Gestao Fundiaria indisponivel para criar loteamento. Verifique a integracao do modulo.')
    if not service.has_financas_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Financas indisponivel para calcular taxas de loteamento. Verifique a integracao do modulo.')
    if not service.has_workflow_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Workflow indisponivel para iniciar fluxo do loteamento. Verifique a integracao do modulo.')

def _ensure_loteamento_aprovacao_adapters(service: LoteamentoService) -> None:
    if not service.has_ambiente_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Ambiente indisponivel para aprovacao do loteamento.')
    if not service.has_obras_publicas_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Obras Publicas indisponivel para aprovacao do loteamento.')
    if not service.has_aguas_saneamento_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Aguas e Saneamento indisponivel para aprovacao do loteamento.')
    if not service.has_transportes_adapter():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Transportes indisponivel para aprovacao do loteamento.')

@router.post('/', response_model=LoteamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_loteamento(data: LoteamentoCreate, service: LoteamentoService=Depends(get_loteamento_service)):
    _ensure_loteamento_create_adapters(service)
    try:
        return await service.criar(nome=data.nome, tipo=data.tipo, parcelamento_id=data.parcelamento_id, plano_diretor_id=data.plano_diretor_id, zoneamento_id=data.zoneamento_id, provincia=data.provincia, area_total=data.area_total, quantidade_lotes_prevista=data.quantidade_lotes_prevista, municipio=data.municipio, area_lotes=data.area_lotes, area_verde=data.area_verde, area_institucional=data.area_institucional, data_inicio_prevista=data.data_inicio_prevista, data_fim_prevista=data.data_fim_prevista, codigo_loteamento=data.codigo_loteamento)
    except LoteamentoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_loteamento:path}/aprovar', response_model=LoteamentoResponse)
async def aprovar_loteamento(codigo_loteamento: str, service: LoteamentoService=Depends(get_loteamento_service)):
    _ensure_loteamento_aprovacao_adapters(service)
    try:
        return await service.aprovar(codigo_loteamento)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_loteamento:path}/iniciar-implantacao', response_model=LoteamentoResponse)
async def iniciar_implantacao_loteamento(codigo_loteamento: str, data: LoteamentoInicioInput, service: LoteamentoService=Depends(get_loteamento_service)):
    try:
        return await service.iniciar_implantacao(codigo_loteamento, data_inicio_real=data.data_inicio_real)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_loteamento:path}/implantar-lotes', response_model=LoteamentoResponse)
async def registrar_implantacao_loteamento(codigo_loteamento: str, data: LoteamentoImplantacaoInput, service: LoteamentoService=Depends(get_loteamento_service)):
    try:
        return await service.registrar_implantacao(codigo_loteamento, quantidade_lotes_implantada=data.quantidade_lotes_implantada)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_loteamento:path}/concluir', response_model=LoteamentoResponse)
async def concluir_loteamento(codigo_loteamento: str, data: LoteamentoConclusaoInput, service: LoteamentoService=Depends(get_loteamento_service)):
    try:
        return await service.concluir(codigo_loteamento, data_fim_real=data.data_fim_real)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_loteamento:path}/suspender', response_model=LoteamentoResponse)
async def suspender_loteamento(codigo_loteamento: str, data: LoteamentoMotivoInput, service: LoteamentoService=Depends(get_loteamento_service)):
    try:
        return await service.suspender(codigo_loteamento, motivo=data.motivo)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_loteamento:path}/retomar', response_model=LoteamentoResponse)
async def retomar_loteamento(codigo_loteamento: str, service: LoteamentoService=Depends(get_loteamento_service)):
    try:
        return await service.retomar(codigo_loteamento)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_loteamento:path}/cancelar', response_model=LoteamentoResponse)
async def cancelar_loteamento(codigo_loteamento: str, data: LoteamentoMotivoInput, service: LoteamentoService=Depends(get_loteamento_service)):
    try:
        return await service.cancelar(codigo_loteamento, motivo=data.motivo)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_loteamento:path}', response_model=LoteamentoResponse)
async def obter_loteamento(codigo_loteamento: str, service: LoteamentoService=Depends(get_loteamento_service)):
    try:
        return await service.obter_por_codigo(codigo_loteamento)
    except LoteamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[LoteamentoResponse])
async def listar_loteamentos(status_loteamento: StatusLoteamento | None=None, tipo_loteamento: TipoLoteamento | None=None, provincia: str | None=None, service: LoteamentoService=Depends(get_loteamento_service)):
    return await service.listar(status=status_loteamento, tipo=tipo_loteamento, provincia=provincia)