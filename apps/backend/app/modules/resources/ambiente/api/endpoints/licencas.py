from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.ambiente.api.deps import get_licenciamento_service
from apps.backend.app.modules.resources.ambiente.api.schemas.licenca_schema import (
    LicencaCancelamentoInput,
    LicencaCreate,
    LicencaDeferimentoInput,
    LicencaIndeferimentoInput,
    LicencaResponse,
    LicencaSuspensaoInput,
)
from apps.backend.app.modules.resources.ambiente.application.services.licenciamento_service import (
    LicenciamentoService,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusLicenca, TipoLicenca
from apps.backend.app.modules.resources.ambiente.exceptions import (
    CARNotFoundError,
    LicencaAlreadyExistsError,
    LicencaNotFoundError,
)

router = APIRouter(prefix="/licencas", tags=["Ambiente - Licencas"])

licenciamento_service_dep = Depends(get_licenciamento_service)


@router.post("/", response_model=LicencaResponse, status_code=status.HTTP_201_CREATED)
async def requerer_licenca(
    data: LicencaCreate, service: LicenciamentoService = licenciamento_service_dep
):
    try:
        return await service.requerer_licenca(
            numero_car=data.numero_car, tipo=data.tipo, atividade=data.atividade
        )
    except CARNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except LicencaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_licenca:path}/analise", response_model=LicencaResponse)
async def iniciar_analise(
    numero_licenca: str, service: LicenciamentoService = licenciamento_service_dep
):
    try:
        return await service.iniciar_analise(numero_licenca)
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_licenca:path}/deferir", response_model=LicencaResponse)
async def deferir_licenca(
    numero_licenca: str,
    data: LicencaDeferimentoInput,
    service: LicenciamentoService = licenciamento_service_dep,
):
    try:
        return await service.deferir(
            numero_licenca,
            analista_id=data.analista_id,
            data_validade=data.data_validade,
            condicionantes=data.condicionantes,
        )
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_licenca:path}/indeferir", response_model=LicencaResponse)
async def indeferir_licenca(
    numero_licenca: str,
    data: LicencaIndeferimentoInput,
    service: LicenciamentoService = licenciamento_service_dep,
):
    try:
        return await service.indeferir(
            numero_licenca, analista_id=data.analista_id, motivo=data.motivo
        )
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_licenca:path}/suspender", response_model=LicencaResponse)
async def suspender_licenca(
    numero_licenca: str,
    data: LicencaSuspensaoInput,
    service: LicenciamentoService = licenciamento_service_dep,
):
    try:
        return await service.suspender(numero_licenca, motivo=data.motivo)
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_licenca:path}/cancelar", response_model=LicencaResponse)
async def cancelar_licenca(
    numero_licenca: str,
    data: LicencaCancelamentoInput,
    service: LicenciamentoService = licenciamento_service_dep,
):
    try:
        return await service.cancelar(numero_licenca, motivo=data.motivo)
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{numero_licenca:path}", response_model=LicencaResponse)
async def obter_licenca(
    numero_licenca: str, service: LicenciamentoService = licenciamento_service_dep
):
    try:
        return await service.obter_por_numero(numero_licenca)
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[LicencaResponse])
async def listar_licencas(
    numero_car: str | None = None,
    tipo: TipoLicenca | None = None,
    status_licenca: StatusLicenca | None = None,
    service: LicenciamentoService = licenciamento_service_dep,
):
    return await service.listar(numero_car=numero_car, tipo=tipo, status=status_licenca)