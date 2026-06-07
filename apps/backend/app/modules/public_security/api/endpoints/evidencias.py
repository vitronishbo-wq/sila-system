from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.public_security.api.deps import get_evidencia_service
from apps.backend.app.modules.public_security.api.schemas.evidencia_schema import (
    EvidenciaCreate,
    EvidenciaResponse,
    EvidenciaStatusUpdate,
)
from apps.backend.app.modules.public_security.application.services.evidencia_service import (
    EvidenciaService,
)
from apps.backend.app.modules.public_security.domain.enums import StatusEvidencia

router = APIRouter(prefix="/evidencias", tags=["Seguranca Publica - Evidencias"])

evidencia_service_dep = Depends(get_evidencia_service)


@router.post("/", response_model=EvidenciaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_evidencia(
    data: EvidenciaCreate, service: EvidenciaService = evidencia_service_dep
) -> EvidenciaResponse:
    try:
        return await service.registrar_evidencia(
            vestigio_id=data.vestigio_id,
            tipo=data.tipo,
            descricao=data.descricao,
            fonte=data.fonte,
            confiabilidade=data.confiabilidade,
            analisado_por_id=data.analisado_por_id,
            observacoes=data.observacoes,
            citizen_id=data.citizen_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{evidencia_id}", response_model=EvidenciaResponse)
async def obter_evidencia(
    evidencia_id: UUID, service: EvidenciaService = evidencia_service_dep
) -> EvidenciaResponse:
    try:
        return await service.buscar_evidencia(evidencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[EvidenciaResponse])
async def listar_evidencias(
    vestigio_id: UUID | None = None,
    status_evidencia: StatusEvidencia | None = None,
    service: EvidenciaService = evidencia_service_dep,
) -> list[EvidenciaResponse]:
    return await service.listar_evidencias(vestigio_id=vestigio_id, status=status_evidencia)


@router.patch("/{evidencia_id}/status", response_model=EvidenciaResponse)
async def atualizar_status_evidencia(
    evidencia_id: UUID,
    data: EvidenciaStatusUpdate,
    service: EvidenciaService = evidencia_service_dep,
) -> EvidenciaResponse:
    try:
        return await service.atualizar_status(
            evidencia_id=evidencia_id, status=data.status, observacoes=data.observacoes
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{evidencia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_evidencia(
    evidencia_id: UUID, service: EvidenciaService = evidencia_service_dep
) -> None:
    try:
        await service.remover_evidencia(evidencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc