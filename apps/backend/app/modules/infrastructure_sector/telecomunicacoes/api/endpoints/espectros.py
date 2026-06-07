from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.deps import (
    get_espectro_service,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.espectro_schema import (
    EspectroCreate,
    EspectroResponse,
    EspectroStatusUpdate,
    EspectroVincularOutorga,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.espectro_service import (
    EspectroService,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    TipoEspectro,
)

router = APIRouter(prefix="/espectros", tags=["Telecomunicacoes - Espectro"])
espectro_service_dep = Depends(get_espectro_service)


@router.post("/", response_model=EspectroResponse, status_code=status.HTTP_201_CREATED)
async def registrar_espectro(
    data: EspectroCreate, service: EspectroService = espectro_service_dep
) -> EspectroResponse:
    try:
        return await service.registrar_espectro(
            tipo=data.tipo,
            frequencia_inicial_mhz=data.frequencia_inicial_mhz,
            frequencia_final_mhz=data.frequencia_final_mhz,
            servico_principal=data.servico_principal,
            municipio=data.municipio,
            provincia=data.provincia,
            outorga_id=data.outorga_id,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{espectro_id}", response_model=EspectroResponse)
async def obter_espectro(
    espectro_id: UUID, service: EspectroService = espectro_service_dep
) -> EspectroResponse:
    try:
        return await service.buscar_espectro(espectro_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[EspectroResponse])
async def listar_espectros(
    tipo: TipoEspectro | None = None,
    municipio: str | None = None,
    somente_disponiveis: bool = False,
    service: EspectroService = espectro_service_dep,
) -> list[EspectroResponse]:
    return await service.listar_espectros(
        tipo=tipo, municipio=municipio, somente_disponiveis=somente_disponiveis
    )


@router.patch("/{espectro_id}/status", response_model=EspectroResponse)
async def atualizar_status_espectro(
    espectro_id: UUID,
    data: EspectroStatusUpdate,
    service: EspectroService = espectro_service_dep,
) -> EspectroResponse:
    try:
        return await service.atualizar_status(espectro_id=espectro_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{espectro_id}/vincular-outorga", response_model=EspectroResponse)
async def vincular_outorga(
    espectro_id: UUID,
    data: EspectroVincularOutorga,
    service: EspectroService = espectro_service_dep,
) -> EspectroResponse:
    try:
        return await service.vincular_outorga(espectro_id=espectro_id, outorga_id=data.outorga_id)
    except ValueError as exc:
        text = str(exc).lower()
        code = (
            status.HTTP_404_NOT_FOUND if "nao encontrada" in text else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.delete("/{espectro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_espectro(
    espectro_id: UUID, service: EspectroService = espectro_service_dep
) -> None:
    try:
        await service.remover_espectro(espectro_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
