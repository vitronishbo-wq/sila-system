from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.aguas_saneamento.api.deps import get_consumo_service
from apps.backend.app.modules.resources.aguas_saneamento.api.schemas.consumo_schema import (
    ConsumoCreate,
    ConsumoMotivoInput,
    ConsumoResponse,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.consumo_service import (
    ConsumoService,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusConsumo
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import (
    ConsumoAlreadyExistsError,
    ConsumoNotFoundError,
)

router = APIRouter(prefix="/consumo", tags=["Aguas Saneamento - Consumo"])
consumo_service_dep = Depends(get_consumo_service)


@router.post("/", response_model=ConsumoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_consumo(
    data: ConsumoCreate, service: ConsumoService = consumo_service_dep
):
    try:
        return await service.registrar(
            abastecimento_id=data.abastecimento_id,
            titular_id=data.titular_id,
            referencia=data.referencia,
            categoria=data.categoria,
            volume_m3=data.volume_m3,
            unidade_volume=data.unidade_volume,
            hidrometro_id=data.hidrometro_id,
            leitura_anterior=data.leitura_anterior,
            leitura_atual=data.leitura_atual,
            data_leitura=data.data_leitura,
        )
    except ConsumoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_consumo:path}/validar", response_model=ConsumoResponse)
async def validar_consumo(
    codigo_consumo: str, service: ConsumoService = consumo_service_dep
):
    try:
        return await service.validar(codigo_consumo)
    except ConsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_consumo:path}/faturar", response_model=ConsumoResponse)
async def faturar_consumo(
    codigo_consumo: str, service: ConsumoService = consumo_service_dep
):
    try:
        return await service.faturar(codigo_consumo)
    except ConsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_consumo:path}/cancelar", response_model=ConsumoResponse)
async def cancelar_consumo(
    codigo_consumo: str,
    data: ConsumoMotivoInput,
    service: ConsumoService = consumo_service_dep,
):
    try:
        return await service.cancelar(codigo_consumo, motivo=data.motivo)
    except ConsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_consumo:path}", response_model=ConsumoResponse)
async def obter_consumo(
    codigo_consumo: str, service: ConsumoService = consumo_service_dep
):
    try:
        return await service.obter_por_codigo(codigo_consumo)
    except ConsumoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ConsumoResponse])
async def listar_consumos(
    abastecimento_id: UUID | None = None,
    titular_id: UUID | None = None,
    referencia: str | None = None,
    status_consumo: StatusConsumo | None = None,
    service: ConsumoService = consumo_service_dep,
):
    return await service.listar(
        abastecimento_id=abastecimento_id,
        titular_id=titular_id,
        referencia=referencia,
        status=status_consumo,
    )
