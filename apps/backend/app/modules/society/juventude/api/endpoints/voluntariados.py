from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.juventude.api.deps import get_voluntariado_service
from apps.backend.app.modules.society.juventude.api.schemas.voluntariado_schema import (
    VoluntariadoCreate,
    VoluntariadoResponse,
    VoluntariadoStatusUpdate,
)
from apps.backend.app.modules.society.juventude.application.services.voluntariado_service import (
    VoluntariadoService,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusVoluntariado

router = APIRouter(prefix="/voluntariados", tags=["Juventude - Voluntariados"])

voluntariado_service_dep = Depends(get_voluntariado_service)


@router.post("/", response_model=VoluntariadoResponse, status_code=status.HTTP_201_CREATED)
async def iniciar_voluntariado(
    data: VoluntariadoCreate, service: VoluntariadoService = voluntariado_service_dep
) -> VoluntariadoResponse:
    try:
        return await service.iniciar_voluntariado(
            jovem_id=data.jovem_id,
            organizacao=data.organizacao,
            causa=data.causa,
            carga_horaria_total=data.carga_horaria_total,
            data_inicio=data.data_inicio,
            data_fim=data.data_fim,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{voluntariado_id}", response_model=VoluntariadoResponse)
async def obter_voluntariado(
    voluntariado_id: UUID, service: VoluntariadoService = voluntariado_service_dep
) -> VoluntariadoResponse:
    try:
        return await service.buscar_voluntariado(voluntariado_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[VoluntariadoResponse])
async def listar_voluntariados(
    jovem_id: UUID | None = None,
    status_filtro: StatusVoluntariado | None = None,
    service: VoluntariadoService = voluntariado_service_dep,
) -> list[VoluntariadoResponse]:
    return await service.listar_voluntariados(jovem_id=jovem_id, status=status_filtro)


@router.patch("/{voluntariado_id}/status", response_model=VoluntariadoResponse)
async def atualizar_status_voluntariado(
    voluntariado_id: UUID,
    data: VoluntariadoStatusUpdate,
    service: VoluntariadoService = voluntariado_service_dep,
) -> VoluntariadoResponse:
    try:
        return await service.atualizar_status(voluntariado_id=voluntariado_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{voluntariado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_voluntariado(
    voluntariado_id: UUID, service: VoluntariadoService = voluntariado_service_dep
) -> None:
    try:
        await service.remover_voluntariado(voluntariado_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc