from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.public_security.api.deps import get_mandado_service
from apps.backend.app.modules.public_security.api.schemas.mandado_schema import (
    MandadoCreate,
    MandadoResponse,
    MandadoStatusUpdate,
)
from apps.backend.app.modules.public_security.application.services.mandado_service import (
    MandadoService,
)
from apps.backend.app.modules.public_security.domain.enums import StatusMandado, TipoMandado

router = APIRouter(prefix="/mandados", tags=["Seguranca Publica - Mandados"])

mandado_service_dep = Depends(get_mandado_service)


@router.post("/", response_model=MandadoResponse, status_code=status.HTTP_201_CREATED)
async def expedir_mandado(
    data: MandadoCreate, service: MandadoService = mandado_service_dep
) -> MandadoResponse:
    try:
        return await service.expedir_mandado(
            ocorrencia_id=data.ocorrencia_id,
            tipo=data.tipo,
            autoridade_judicial=data.autoridade_judicial,
            data_expedicao=data.data_expedicao,
            data_validade=data.data_validade,
            unidade_id=data.unidade_id,
            policial_responsavel_id=data.policial_responsavel_id,
            observacoes=data.observacoes,
            citizen_id=data.citizen_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{mandado_id}", response_model=MandadoResponse)
async def obter_mandado(
    mandado_id: UUID, service: MandadoService = mandado_service_dep
) -> MandadoResponse:
    try:
        return await service.buscar_mandado(mandado_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[MandadoResponse])
async def listar_mandados(
    ocorrencia_id: UUID | None = None,
    tipo: TipoMandado | None = None,
    status_mandado: StatusMandado | None = None,
    service: MandadoService = mandado_service_dep,
) -> list[MandadoResponse]:
    return await service.listar_mandados(
        ocorrencia_id=ocorrencia_id, tipo=tipo, status=status_mandado
    )


@router.patch("/{mandado_id}/status", response_model=MandadoResponse)
async def atualizar_status_mandado(
    mandado_id: UUID,
    data: MandadoStatusUpdate,
    service: MandadoService = mandado_service_dep,
) -> MandadoResponse:
    try:
        return await service.atualizar_status(
            mandado_id=mandado_id, status=data.status, observacoes=data.observacoes
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{mandado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_mandado(
    mandado_id: UUID, service: MandadoService = mandado_service_dep
) -> None:
    try:
        await service.remover_mandado(mandado_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc