from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header, status
from apps.backend.app.modules.infrastructure.api.deps import get_obra_service
from apps.backend.app.modules.infrastructure.api.schemas.obra_schema import EventStoreEntryResponse, ObraAditivoInput, ObraConclusaoInput, ObraContratacaoInput, ObraCreate, ObraRehydratedStateResponse, ObraEntregaInput, ObraFiscalizacaoInput, ObraInicioExecucaoInput, ObraMedicaoDetalhadaInput, ObraProgressoInput, ObraResponse, ObraSuspensaoInput, ObraTermoRecebimentoInput, ObraValorInput
from apps.backend.app.modules.infrastructure.application.services.obra_service import ObraService
from apps.backend.app.modules.infrastructure.domain.enums import StatusObra
from apps.backend.app.modules.infrastructure.domain.exceptions import ObraAlreadyExistsError, ObraNotFoundError
router = APIRouter(prefix='/obras', tags=['Obras Publicas - Obras'])

def _resolve_request_context(*, x_tenant_id: str | None, x_correlation_id: str | None) -> tuple[str, str | None]:
    tenant_id = (x_tenant_id or '').strip() or 'default'
    correlation_id = (x_correlation_id or '').strip() or None
    return (tenant_id, correlation_id)

def _has_capability(service: ObraService, method_name: str) -> bool:
    checker = getattr(service, method_name, None)
    if checker is None:
        return True
    return bool(checker())

def _ensure_criacao_adapters(service: ObraService) -> None:
    if not _has_capability(service, 'has_urbanismo_habitacao_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Urbanismo Habitacao indisponivel para criacao da obra.')
    if not _has_capability(service, 'has_workflow_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Workflow indisponivel para criacao da obra.')
    if not _has_capability(service, 'has_service_requests_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Service Requests indisponivel para criacao da obra.')

def _ensure_execucao_adapters(service: ObraService) -> None:
    if not _has_capability(service, 'has_ambiente_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Ambiente indisponivel para inicio de execucao da obra.')
    if not _has_capability(service, 'has_transportes_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Transportes indisponivel para inicio de execucao da obra.')
    if not _has_capability(service, 'has_aguas_saneamento_adapter'):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Adapter de Aguas e Saneamento indisponivel para inicio de execucao da obra.')

@router.post('/', response_model=ObraResponse, status_code=status.HTTP_201_CREATED)
async def criar_obra(data: ObraCreate, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), x_correlation_id: str | None=Header(default=None, alias='X-Correlation-ID'), service: ObraService=Depends(get_obra_service)):
    tenant_id, correlation_id = _resolve_request_context(x_tenant_id=x_tenant_id, x_correlation_id=x_correlation_id)
    _ensure_criacao_adapters(service)
    try:
        return await service.criar(nome=data.nome, tipo=data.tipo, natureza=data.natureza, orgao_responsavel_id=data.orgao_responsavel_id, orgao_responsavel_tipo=data.orgao_responsavel_tipo, valor_orcado=data.valor_orcado, data_inicio_prevista=data.data_inicio_prevista, data_fim_prevista=data.data_fim_prevista, endereco=data.endereco, bairro=data.bairro, municipio=data.municipio, provincia=data.provincia, codigo_obra=data.codigo_obra, descricao=data.descricao, tenant_id=tenant_id, correlation_id=correlation_id)
    except ObraAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/iniciar-licitacao', response_model=ObraResponse)
async def iniciar_licitacao_obra(codigo_obra: str, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.iniciar_licitacao(codigo_obra)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/contratar', response_model=ObraResponse)
async def contratar_obra(codigo_obra: str, data: ObraContratacaoInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.contratar(codigo_obra, contrato_id=data.contrato_id, empreiteira_id=data.empreiteira_id, valor=data.valor_contratado)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/iniciar-execucao', response_model=ObraResponse)
async def iniciar_execucao_obra(codigo_obra: str, data: ObraInicioExecucaoInput, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), x_correlation_id: str | None=Header(default=None, alias='X-Correlation-ID'), service: ObraService=Depends(get_obra_service)):
    tenant_id, correlation_id = _resolve_request_context(x_tenant_id=x_tenant_id, x_correlation_id=x_correlation_id)
    _ensure_execucao_adapters(service)
    try:
        return await service.iniciar_execucao(codigo_obra, data_inicio=data.data_inicio, tenant_id=tenant_id, correlation_id=correlation_id)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/progresso', response_model=ObraResponse)
async def atualizar_progresso_obra(codigo_obra: str, data: ObraProgressoInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.atualizar_progresso(codigo_obra, percentual=data.percentual)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/medicao', response_model=ObraResponse)
async def registrar_medicao_obra(codigo_obra: str, data: ObraValorInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.registrar_medicao(codigo_obra, valor=data.valor)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/medicao-detalhada', response_model=ObraResponse)
async def registrar_medicao_detalhada_obra(codigo_obra: str, data: ObraMedicaoDetalhadaInput, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), x_correlation_id: str | None=Header(default=None, alias='X-Correlation-ID'), service: ObraService=Depends(get_obra_service)):
    tenant_id, correlation_id = _resolve_request_context(x_tenant_id=x_tenant_id, x_correlation_id=x_correlation_id)
    try:
        return await service.registrar_medicao_detalhada(codigo_obra, periodo_referencia=data.periodo_referencia, valor_medido=data.valor_medido, percentual_executado=data.percentual_executado, fiscal_id=data.fiscal_id, documentos=data.documentos, observacoes=data.observacoes, data_medicao=data.data_medicao, tenant_id=tenant_id, correlation_id=correlation_id)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/pagamento', response_model=ObraResponse)
async def registrar_pagamento_obra(codigo_obra: str, data: ObraValorInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.registrar_pagamento(codigo_obra, valor=data.valor)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/aditivo', response_model=ObraResponse)
async def registrar_aditivo_obra(codigo_obra: str, data: ObraAditivoInput, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), x_correlation_id: str | None=Header(default=None, alias='X-Correlation-ID'), service: ObraService=Depends(get_obra_service)):
    tenant_id, correlation_id = _resolve_request_context(x_tenant_id=x_tenant_id, x_correlation_id=x_correlation_id)
    try:
        return await service.registrar_aditivo(codigo_obra, tipo=data.tipo, justificativa=data.justificativa, valor_aditivo=data.valor_aditivo, prazo_adicional_dias=data.prazo_adicional_dias, data_assinatura=data.data_assinatura, tenant_id=tenant_id, correlation_id=correlation_id)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/fiscalizacao', response_model=ObraResponse)
async def registrar_fiscalizacao_obra(codigo_obra: str, data: ObraFiscalizacaoInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.registrar_fiscalizacao(codigo_obra, fiscal_id=data.fiscal_id, conformidade=data.conformidade, apontamentos=data.apontamentos, recomendacoes=data.recomendacoes, data_fiscalizacao=data.data_fiscalizacao)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/suspender', response_model=ObraResponse)
async def suspender_obra(codigo_obra: str, data: ObraSuspensaoInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.suspender(codigo_obra, motivo=data.motivo)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/termo-recebimento', response_model=ObraResponse)
async def registrar_termo_recebimento_obra(codigo_obra: str, data: ObraTermoRecebimentoInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.registrar_termo_recebimento(codigo_obra, tipo=data.tipo, responsavel_id=data.responsavel_id, data_termo=data.data_termo, observacoes=data.observacoes)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/retomar', response_model=ObraResponse)
async def retomar_obra(codigo_obra: str, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.retomar(codigo_obra)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/concluir', response_model=ObraResponse)
async def concluir_obra(codigo_obra: str, data: ObraConclusaoInput, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), x_correlation_id: str | None=Header(default=None, alias='X-Correlation-ID'), service: ObraService=Depends(get_obra_service)):
    tenant_id, correlation_id = _resolve_request_context(x_tenant_id=x_tenant_id, x_correlation_id=x_correlation_id)
    try:
        return await service.concluir(codigo_obra, data_conclusao=data.data_conclusao, tenant_id=tenant_id, correlation_id=correlation_id)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_obra:path}/entregar', response_model=ObraResponse)
async def entregar_obra(codigo_obra: str, data: ObraEntregaInput, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.entregar(codigo_obra, data_entrega=data.data_entrega)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_obra:path}/event-stream', response_model=list[EventStoreEntryResponse])
async def obter_event_stream_obra(codigo_obra: str, tenant_id: str | None=None, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), service: ObraService=Depends(get_obra_service)):
    effective_tenant = (tenant_id or x_tenant_id or '').strip() or None
    try:
        return await service.obter_event_stream(codigo_obra, tenant_id=effective_tenant)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/{codigo_obra:path}/rehydrate', response_model=ObraRehydratedStateResponse | dict)
async def rehidratar_obra_por_eventos(codigo_obra: str, tenant_id: str | None=None, x_tenant_id: str | None=Header(default=None, alias='X-Tenant-ID'), service: ObraService=Depends(get_obra_service)):
    effective_tenant = (tenant_id or x_tenant_id or '').strip() or None
    try:
        return await service.rehidratar_estado_obra(codigo_obra, tenant_id=effective_tenant)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/{codigo_obra:path}', response_model=ObraResponse)
async def obter_obra(codigo_obra: str, service: ObraService=Depends(get_obra_service)):
    try:
        return await service.obter_por_codigo(codigo_obra)
    except ObraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ObraResponse])
async def listar_obras(status_obra: StatusObra | None=None, orgao_responsavel_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None, service: ObraService=Depends(get_obra_service)):
    return await service.listar(status=status_obra, orgao_responsavel_id=orgao_responsavel_id, municipio=municipio, provincia=provincia)
