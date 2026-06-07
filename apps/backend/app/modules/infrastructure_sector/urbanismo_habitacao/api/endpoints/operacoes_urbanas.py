from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import (
    get_operacao_urbana_service,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.operacao_urbana_schema import (
    OperacaoUrbanaConclusaoInput,
    OperacaoUrbanaCreate,
    OperacaoUrbanaExecucaoInput,
    OperacaoUrbanaInicioInput,
    OperacaoUrbanaMotivoInput,
    OperacaoUrbanaResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.operacao_urbana_service import (
    OperacaoUrbanaService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusOperacaoUrbana,
    TipoOperacaoUrbana,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import (
    OperacaoUrbanaAlreadyExistsError,
    OperacaoUrbanaNotFoundError,
)

router = APIRouter(prefix="/operacoes-urbanas", tags=["Urbanismo Habitacao - Operacoes Urbanas"])
operacao_urbana_service_dep = Depends(get_operacao_urbana_service)


@router.post("/", response_model=OperacaoUrbanaResponse, status_code=status.HTTP_201_CREATED)
async def criar_operacao_urbana(
    data: OperacaoUrbanaCreate,
    service: OperacaoUrbanaService = operacao_urbana_service_dep,
):
    try:
        return await service.criar(
            nome=data.nome,
            tipo=data.tipo,
            plano_diretor_id=data.plano_diretor_id,
            orgao_responsavel_id=data.orgao_responsavel_id,
            provincia=data.provincia,
            municipio=data.municipio,
            area_intervencao=data.area_intervencao,
            investimento_previsto=data.investimento_previsto,
            data_inicio_prevista=data.data_inicio_prevista,
            data_fim_prevista=data.data_fim_prevista,
            codigo_operacao=data.codigo_operacao,
        )
    except OperacaoUrbanaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_operacao:path}/aprovar", response_model=OperacaoUrbanaResponse)
async def aprovar_operacao_urbana(
    codigo_operacao: str, service: OperacaoUrbanaService = operacao_urbana_service_dep
):
    try:
        return await service.aprovar(codigo_operacao)
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_operacao:path}/iniciar-execucao", response_model=OperacaoUrbanaResponse)
async def iniciar_execucao_operacao_urbana(
    codigo_operacao: str,
    data: OperacaoUrbanaInicioInput,
    service: OperacaoUrbanaService = operacao_urbana_service_dep,
):
    try:
        return await service.iniciar_execucao(
            codigo_operacao, data_inicio_real=data.data_inicio_real
        )
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_operacao:path}/execucao", response_model=OperacaoUrbanaResponse)
async def atualizar_execucao_operacao_urbana(
    codigo_operacao: str,
    data: OperacaoUrbanaExecucaoInput,
    service: OperacaoUrbanaService = operacao_urbana_service_dep,
):
    try:
        return await service.atualizar_execucao(
            codigo_operacao,
            percentual_execucao=data.percentual_execucao,
            investimento_executado=data.investimento_executado,
        )
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_operacao:path}/concluir", response_model=OperacaoUrbanaResponse)
async def concluir_operacao_urbana(
    codigo_operacao: str,
    data: OperacaoUrbanaConclusaoInput,
    service: OperacaoUrbanaService = operacao_urbana_service_dep,
):
    try:
        return await service.concluir(codigo_operacao, data_fim_real=data.data_fim_real)
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_operacao:path}/suspender", response_model=OperacaoUrbanaResponse)
async def suspender_operacao_urbana(
    codigo_operacao: str,
    data: OperacaoUrbanaMotivoInput,
    service: OperacaoUrbanaService = operacao_urbana_service_dep,
):
    try:
        return await service.suspender(codigo_operacao, motivo=data.motivo)
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_operacao:path}/retomar", response_model=OperacaoUrbanaResponse)
async def retomar_operacao_urbana(
    codigo_operacao: str, service: OperacaoUrbanaService = operacao_urbana_service_dep
):
    try:
        return await service.retomar(codigo_operacao)
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_operacao:path}/cancelar", response_model=OperacaoUrbanaResponse)
async def cancelar_operacao_urbana(
    codigo_operacao: str,
    data: OperacaoUrbanaMotivoInput,
    service: OperacaoUrbanaService = operacao_urbana_service_dep,
):
    try:
        return await service.cancelar(codigo_operacao, motivo=data.motivo)
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_operacao:path}", response_model=OperacaoUrbanaResponse)
async def obter_operacao_urbana(
    codigo_operacao: str, service: OperacaoUrbanaService = operacao_urbana_service_dep
):
    try:
        return await service.obter_por_codigo(codigo_operacao)
    except OperacaoUrbanaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[OperacaoUrbanaResponse])
async def listar_operacoes_urbanas(
    status_operacao: StatusOperacaoUrbana | None = None,
    tipo_operacao: TipoOperacaoUrbana | None = None,
    provincia: str | None = None,
    service: OperacaoUrbanaService = operacao_urbana_service_dep,
):
    return await service.listar(status=status_operacao, tipo=tipo_operacao, provincia=provincia)
