from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import (
    get_alvara_service,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.alvara_schema import (
    AlvaraCreate,
    AlvaraDeferimentoInput,
    AlvaraMotivoInput,
    AlvaraResponse,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.alvara_service import (
    AlvaraService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusAlvara,
    TipoAlvara,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import (
    AlvaraAlreadyExistsError,
    AlvaraNotFoundError,
)

router = APIRouter(prefix="/alvaras", tags=["Urbanismo Habitacao - Alvaras"])
alvara_service_dep = Depends(get_alvara_service)


@router.post("/", response_model=AlvaraResponse, status_code=status.HTTP_201_CREATED)
async def criar_alvara(data: AlvaraCreate, service: AlvaraService = alvara_service_dep):
    try:
        return await service.criar(
            numero_processo=data.numero_processo,
            tipo=data.tipo,
            licenca_urbanistica_id=data.licenca_urbanistica_id,
            requerente_id=data.requerente_id,
            provincia=data.provincia,
            municipio=data.municipio,
            endereco_obra=data.endereco_obra,
            area_autorizada=data.area_autorizada,
            codigo_alvara=data.codigo_alvara,
        )
    except AlvaraAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_alvara:path}/analise", response_model=AlvaraResponse)
async def iniciar_analise_alvara(
    codigo_alvara: str, service: AlvaraService = alvara_service_dep
):
    try:
        return await service.iniciar_analise(codigo_alvara)
    except AlvaraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_alvara:path}/pendencia", response_model=AlvaraResponse)
async def registrar_pendencia_alvara(
    codigo_alvara: str,
    data: AlvaraMotivoInput,
    service: AlvaraService = alvara_service_dep,
):
    try:
        return await service.solicitar_pendencia(codigo_alvara, motivo=data.motivo)
    except AlvaraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_alvara:path}/deferir", response_model=AlvaraResponse)
async def deferir_alvara(
    codigo_alvara: str,
    data: AlvaraDeferimentoInput,
    service: AlvaraService = alvara_service_dep,
):
    try:
        return await service.deferir(
            codigo_alvara,
            data_emissao=data.data_emissao,
            data_validade=data.data_validade,
            analista_id=data.analista_id,
        )
    except AlvaraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_alvara:path}/indeferir", response_model=AlvaraResponse)
async def indeferir_alvara(
    codigo_alvara: str,
    data: AlvaraMotivoInput,
    service: AlvaraService = alvara_service_dep,
):
    try:
        return await service.indeferir(codigo_alvara, motivo=data.motivo)
    except AlvaraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_alvara:path}/cancelar", response_model=AlvaraResponse)
async def cancelar_alvara(
    codigo_alvara: str,
    data: AlvaraMotivoInput,
    service: AlvaraService = alvara_service_dep,
):
    try:
        return await service.cancelar(codigo_alvara, motivo=data.motivo)
    except AlvaraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_alvara:path}", response_model=AlvaraResponse)
async def obter_alvara(codigo_alvara: str, service: AlvaraService = alvara_service_dep):
    try:
        return await service.obter_por_codigo(codigo_alvara)
    except AlvaraNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[AlvaraResponse])
async def listar_alvaras(
    status_alvara: StatusAlvara | None = None,
    tipo_alvara: TipoAlvara | None = None,
    provincia: str | None = None,
    service: AlvaraService = alvara_service_dep,
):
    return await service.listar(status=status_alvara, tipo=tipo_alvara, provincia=provincia)
