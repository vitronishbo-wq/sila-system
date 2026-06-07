from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.public_security.api.deps import get_prova_pericial_service
from apps.backend.app.modules.public_security.api.schemas.prova_pericial_schema import (
    ProvaPericialCreate,
    ProvaPericialResponse,
    ProvaPericialStatusUpdate,
    ProvaPericialVinculoCadeia,
)
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import (
    ProvaPericialService,
)
from apps.backend.app.modules.public_security.domain.enums import StatusProva, TipoProva

router = APIRouter(prefix="/provas-periciais", tags=["Seguranca Publica - Provas Periciais"])

prova_pericial_service_dep = Depends(get_prova_pericial_service)


@router.post("/", response_model=ProvaPericialResponse, status_code=status.HTTP_201_CREATED)
async def coletar_prova(
    data: ProvaPericialCreate, service: ProvaPericialService = prova_pericial_service_dep
) -> ProvaPericialResponse:
    try:
        return await service.coletar_prova(
            ocorrencia_id=data.ocorrencia_id,
            tipo=data.tipo,
            descricao=data.descricao,
            local_coleta=data.local_coleta,
            data_coleta=data.data_coleta,
            coletado_por_id=data.coletado_por_id,
            observacoes=data.observacoes,
            citizen_id=data.citizen_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{prova_id}", response_model=ProvaPericialResponse)
async def obter_prova(
    prova_id: UUID, service: ProvaPericialService = prova_pericial_service_dep
) -> ProvaPericialResponse:
    try:
        return await service.buscar_prova(prova_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ProvaPericialResponse])
async def listar_provas(
    ocorrencia_id: UUID | None = None,
    tipo: TipoProva | None = None,
    status_prova: StatusProva | None = None,
    service: ProvaPericialService = prova_pericial_service_dep,
) -> list[ProvaPericialResponse]:
    return await service.listar_provas(ocorrencia_id=ocorrencia_id, tipo=tipo, status=status_prova)


@router.patch("/{prova_id}/status", response_model=ProvaPericialResponse)
async def atualizar_status_prova(
    prova_id: UUID,
    data: ProvaPericialStatusUpdate,
    service: ProvaPericialService = prova_pericial_service_dep,
) -> ProvaPericialResponse:
    try:
        return await service.atualizar_status(
            prova_id=prova_id, status=data.status, observacoes=data.observacoes
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{prova_id}/cadeia-custodia", response_model=ProvaPericialResponse)
async def vincular_cadeia_custodia(
    prova_id: UUID,
    data: ProvaPericialVinculoCadeia,
    service: ProvaPericialService = prova_pericial_service_dep,
) -> ProvaPericialResponse:
    try:
        return await service.vincular_cadeia_custodia(
            prova_id=prova_id, cadeia_custodia_id=data.cadeia_custodia_id
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{prova_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_prova(
    prova_id: UUID, service: ProvaPericialService = prova_pericial_service_dep
) -> None:
    try:
        await service.remover_prova(prova_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc