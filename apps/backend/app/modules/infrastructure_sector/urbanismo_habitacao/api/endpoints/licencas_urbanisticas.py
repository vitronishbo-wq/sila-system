from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import (
    get_licenciamento_urbano_service,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.licenca_urbanistica_schema import (
    LicencaUrbanisticaCreate,
    LicencaUrbanisticaDeferimentoInput,
    LicencaUrbanisticaMotivoInput,
    LicencaUrbanisticaResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.licenciamento_urbano_service import (
    LicenciamentoUrbanoService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusLicencaUrbanistica,
    TipoAlvara,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import (
    LicencaUrbanisticaAlreadyExistsError,
    LicencaUrbanisticaNotFoundError,
)

router = APIRouter(
    prefix="/licencas-urbanisticas", tags=["Urbanismo Habitacao - Licenciamento Urbanistico"]
)
licenciamento_urbano_service_dep = Depends(get_licenciamento_urbano_service)


def _ensure_deferimento_adapters(service: LicenciamentoUrbanoService) -> None:
    if not service.has_ambiente_adapter():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Adapter de Ambiente indisponivel para deferimento da licenca.",
        )
    if not service.has_financas_adapter():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Adapter de Financas indisponivel para cobranca da licenca.",
        )
    if not service.has_workflow_adapter():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Adapter de Workflow indisponivel para deferimento da licenca.",
        )


@router.post("/", response_model=LicencaUrbanisticaResponse, status_code=status.HTTP_201_CREATED)
async def criar_licenca_urbanistica(
    data: LicencaUrbanisticaCreate,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    try:
        return await service.criar(
            numero_processo=data.numero_processo,
            tipo_alvara=data.tipo_alvara,
            requerente_id=data.requerente_id,
            zoneamento_id=data.zoneamento_id,
            provincia=data.provincia,
            municipio=data.municipio,
            endereco_obra=data.endereco_obra,
            area_construida_prevista=data.area_construida_prevista,
            codigo_licenca=data.codigo_licenca,
        )
    except LicencaUrbanisticaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_licenca:path}/analise", response_model=LicencaUrbanisticaResponse)
async def iniciar_analise_licenca_urbanistica(
    codigo_licenca: str,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    try:
        return await service.iniciar_analise(codigo_licenca)
    except LicencaUrbanisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_licenca:path}/pendencia", response_model=LicencaUrbanisticaResponse)
async def registrar_pendencia_licenca_urbanistica(
    codigo_licenca: str,
    data: LicencaUrbanisticaMotivoInput,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    try:
        return await service.solicitar_pendencia(codigo_licenca, motivo=data.motivo)
    except LicencaUrbanisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_licenca:path}/deferir", response_model=LicencaUrbanisticaResponse)
async def deferir_licenca_urbanistica(
    codigo_licenca: str,
    data: LicencaUrbanisticaDeferimentoInput,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    _ensure_deferimento_adapters(service)
    try:
        return await service.deferir(
            codigo_licenca,
            data_emissao=data.data_emissao,
            data_validade=data.data_validade,
            tecnico_responsavel_id=data.tecnico_responsavel_id,
        )
    except LicencaUrbanisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_licenca:path}/indeferir", response_model=LicencaUrbanisticaResponse)
async def indeferir_licenca_urbanistica(
    codigo_licenca: str,
    data: LicencaUrbanisticaMotivoInput,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    try:
        return await service.indeferir(codigo_licenca, motivo=data.motivo)
    except LicencaUrbanisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_licenca:path}/cancelar", response_model=LicencaUrbanisticaResponse)
async def cancelar_licenca_urbanistica(
    codigo_licenca: str,
    data: LicencaUrbanisticaMotivoInput,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    try:
        return await service.cancelar(codigo_licenca, motivo=data.motivo)
    except LicencaUrbanisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_licenca:path}", response_model=LicencaUrbanisticaResponse)
async def obter_licenca_urbanistica(
    codigo_licenca: str,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    try:
        return await service.obter_por_codigo(codigo_licenca)
    except LicencaUrbanisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[LicencaUrbanisticaResponse])
async def listar_licencas_urbanisticas(
    status_licenca: StatusLicencaUrbanistica | None = None,
    tipo_alvara: TipoAlvara | None = None,
    provincia: str | None = None,
    service: LicenciamentoUrbanoService = licenciamento_urbano_service_dep,
):
    return await service.listar(status=status_licenca, tipo_alvara=tipo_alvara, provincia=provincia)
