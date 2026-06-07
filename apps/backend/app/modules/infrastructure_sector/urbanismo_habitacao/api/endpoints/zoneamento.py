from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import (
    get_zoneamento_service,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.zoneamento_schema import (
    ZoneamentoCreate,
    ZoneamentoMotivoInput,
    ZoneamentoParametrosInput,
    ZoneamentoResponse,
    ZoneamentoVigenciaInput,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.zoneamento_service import (
    ZoneamentoService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusZoneamento,
    TipoZona,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import (
    ZoneamentoAlreadyExistsError,
    ZoneamentoNotFoundError,
)

router = APIRouter(prefix="/zoneamento", tags=["Urbanismo Habitacao - Zoneamento"])
zoneamento_service_dep = Depends(get_zoneamento_service)


@router.post("/", response_model=ZoneamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_zoneamento(
    data: ZoneamentoCreate, service: ZoneamentoService = zoneamento_service_dep
):
    try:
        return await service.criar(
            nome=data.nome,
            tipo_zona=data.tipo_zona,
            plano_diretor_id=data.plano_diretor_id,
            provincia=data.provincia,
            usos_permitidos=data.usos_permitidos,
            municipio=data.municipio,
            codigo_zoneamento=data.codigo_zoneamento,
        )
    except ZoneamentoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_zoneamento:path}/consulta-publica", response_model=ZoneamentoResponse)
async def iniciar_consulta_publica(
    codigo_zoneamento: str, service: ZoneamentoService = zoneamento_service_dep
):
    try:
        return await service.iniciar_consulta_publica(codigo_zoneamento)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_zoneamento:path}/aprovar", response_model=ZoneamentoResponse)
async def aprovar_zoneamento(
    codigo_zoneamento: str, service: ZoneamentoService = zoneamento_service_dep
):
    try:
        return await service.aprovar(codigo_zoneamento)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_zoneamento:path}/vigorar", response_model=ZoneamentoResponse)
async def vigorar_zoneamento(
    codigo_zoneamento: str,
    data: ZoneamentoVigenciaInput,
    service: ZoneamentoService = zoneamento_service_dep,
):
    try:
        return await service.vigorar(
            codigo_zoneamento, data_inicio_vigencia=data.data_inicio_vigencia
        )
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_zoneamento:path}/suspender", response_model=ZoneamentoResponse)
async def suspender_zoneamento(
    codigo_zoneamento: str,
    data: ZoneamentoMotivoInput,
    service: ZoneamentoService = zoneamento_service_dep,
):
    try:
        return await service.suspender(codigo_zoneamento, motivo=data.motivo)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_zoneamento:path}/revogar", response_model=ZoneamentoResponse)
async def revogar_zoneamento(
    codigo_zoneamento: str,
    data: ZoneamentoMotivoInput,
    service: ZoneamentoService = zoneamento_service_dep,
):
    try:
        return await service.revogar(codigo_zoneamento, motivo=data.motivo)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_zoneamento:path}/parametros", response_model=ZoneamentoResponse)
async def atualizar_parametros_zoneamento(
    codigo_zoneamento: str,
    data: ZoneamentoParametrosInput,
    service: ZoneamentoService = zoneamento_service_dep,
):
    try:
        return await service.atualizar_parametros(
            codigo_zoneamento,
            usos_permitidos=data.usos_permitidos,
            coeficiente_aproveitamento_max=data.coeficiente_aproveitamento_max,
            taxa_ocupacao_max=data.taxa_ocupacao_max,
            gabarito_maximo=data.gabarito_maximo,
            recuo_frontal_minimo=data.recuo_frontal_minimo,
            permeabilidade_minima=data.permeabilidade_minima,
            area_lote_minima=data.area_lote_minima,
        )
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_zoneamento:path}", response_model=ZoneamentoResponse)
async def obter_zoneamento(
    codigo_zoneamento: str, service: ZoneamentoService = zoneamento_service_dep
):
    try:
        return await service.obter_por_codigo(codigo_zoneamento)
    except ZoneamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ZoneamentoResponse])
async def listar_zoneamentos(
    status_zoneamento: StatusZoneamento | None = None,
    tipo_zona: TipoZona | None = None,
    provincia: str | None = None,
    service: ZoneamentoService = zoneamento_service_dep,
):
    return await service.listar(status=status_zoneamento, tipo_zona=tipo_zona, provincia=provincia)
