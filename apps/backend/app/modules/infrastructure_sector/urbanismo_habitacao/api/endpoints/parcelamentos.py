from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import (
    get_parcelamento_service,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.parcelamento_schema import (
    ParcelamentoConclusaoInput,
    ParcelamentoCreate,
    ParcelamentoMotivoInput,
    ParcelamentoResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.parcelamento_service import (
    ParcelamentoService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusParcelamento,
    TipoParcelamento,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import (
    ParcelamentoAlreadyExistsError,
    ParcelamentoNotFoundError,
)

router = APIRouter(prefix="/parcelamentos", tags=["Urbanismo Habitacao - Parcelamentos"])
parcelamento_service_dep = Depends(get_parcelamento_service)


@router.post("/", response_model=ParcelamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_parcelamento(
    data: ParcelamentoCreate, service: ParcelamentoService = parcelamento_service_dep
):
    try:
        return await service.criar(
            nome=data.nome,
            tipo=data.tipo,
            plano_diretor_id=data.plano_diretor_id,
            zoneamento_id=data.zoneamento_id,
            provincia=data.provincia,
            area_total=data.area_total,
            quantidade_unidades_prevista=data.quantidade_unidades_prevista,
            municipio=data.municipio,
            area_publica_prevista=data.area_publica_prevista,
            area_sistema_viario_prevista=data.area_sistema_viario_prevista,
            codigo_parcelamento=data.codigo_parcelamento,
        )
    except ParcelamentoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_parcelamento:path}/analise", response_model=ParcelamentoResponse)
async def iniciar_analise_parcelamento(
    codigo_parcelamento: str, service: ParcelamentoService = parcelamento_service_dep
):
    try:
        return await service.iniciar_analise(codigo_parcelamento)
    except ParcelamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_parcelamento:path}/aprovar", response_model=ParcelamentoResponse)
async def aprovar_parcelamento(
    codigo_parcelamento: str, service: ParcelamentoService = parcelamento_service_dep
):
    try:
        return await service.aprovar(codigo_parcelamento)
    except ParcelamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_parcelamento:path}/iniciar-execucao", response_model=ParcelamentoResponse)
async def iniciar_execucao_parcelamento(
    codigo_parcelamento: str, service: ParcelamentoService = parcelamento_service_dep
):
    try:
        return await service.iniciar_execucao(codigo_parcelamento)
    except ParcelamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_parcelamento:path}/concluir", response_model=ParcelamentoResponse)
async def concluir_parcelamento(
    codigo_parcelamento: str,
    data: ParcelamentoConclusaoInput,
    service: ParcelamentoService = parcelamento_service_dep,
):
    try:
        return await service.concluir(
            codigo_parcelamento, quantidade_unidades_resultante=data.quantidade_unidades_resultante
        )
    except ParcelamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_parcelamento:path}/cancelar", response_model=ParcelamentoResponse)
async def cancelar_parcelamento(
    codigo_parcelamento: str,
    data: ParcelamentoMotivoInput,
    service: ParcelamentoService = parcelamento_service_dep,
):
    try:
        return await service.cancelar(codigo_parcelamento, motivo=data.motivo)
    except ParcelamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_parcelamento:path}", response_model=ParcelamentoResponse)
async def obter_parcelamento(
    codigo_parcelamento: str, service: ParcelamentoService = parcelamento_service_dep
):
    try:
        return await service.obter_por_codigo(codigo_parcelamento)
    except ParcelamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ParcelamentoResponse])
async def listar_parcelamentos(
    status_parcelamento: StatusParcelamento | None = None,
    tipo_parcelamento: TipoParcelamento | None = None,
    provincia: str | None = None,
    service: ParcelamentoService = parcelamento_service_dep,
):
    return await service.listar(
        status=status_parcelamento, tipo=tipo_parcelamento, provincia=provincia
    )
