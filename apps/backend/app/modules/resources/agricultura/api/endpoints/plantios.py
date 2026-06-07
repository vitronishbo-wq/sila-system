from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_plantio_service
from apps.backend.app.modules.resources.agricultura.api.schemas.plantio_schema import (
    PlantioCancelamentoInput,
    PlantioCreate,
    PlantioResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.plantio_service import (
    PlantioService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusPlantio
from apps.backend.app.modules.resources.agricultura.exceptions import (
    PlantioNotFoundError,
    SafraNotFoundError,
    TalhaoNotFoundError,
)

router = APIRouter(prefix="/plantios", tags=["Agricultura - plantios"])
plantio_service_dep = Depends(get_plantio_service)


@router.post("/", response_model=PlantioResponse, status_code=status.HTTP_201_CREATED)
async def planejar_plantio(
    data: PlantioCreate, service: PlantioService = plantio_service_dep
):
    try:
        return await service.planejar(
            codigo_safra=data.codigo_safra,
            codigo_talhao=data.codigo_talhao,
            area_plantada_ha=data.area_plantada_ha,
            quantidade_semente=data.quantidade_semente,
        )
    except (SafraNotFoundError, TalhaoNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plantio:path}/executar", response_model=PlantioResponse)
async def executar_plantio(
    codigo_plantio: str, service: PlantioService = plantio_service_dep
):
    try:
        return await service.executar(codigo_plantio)
    except PlantioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plantio:path}/cancelar", response_model=PlantioResponse)
async def cancelar_plantio(
    codigo_plantio: str,
    data: PlantioCancelamentoInput,
    service: PlantioService = plantio_service_dep,
):
    try:
        return await service.cancelar(codigo_plantio, motivo=data.motivo)
    except PlantioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_plantio:path}", response_model=PlantioResponse)
async def obter_plantio(
    codigo_plantio: str, service: PlantioService = plantio_service_dep
):
    try:
        return await service.obter(codigo_plantio)
    except PlantioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[PlantioResponse])
async def listar_plantios(
    codigo_safra: str | None = None,
    codigo_talhao: str | None = None,
    status_plantio: StatusPlantio | None = None,
    service: PlantioService = plantio_service_dep,
):
    return await service.listar(
        codigo_safra=codigo_safra, codigo_talhao=codigo_talhao, status=status_plantio
    )
