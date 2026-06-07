from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.juventude.api.deps import get_bolsa_estudo_service
from apps.backend.app.modules.society.juventude.api.schemas.bolsa_estudo_schema import (
    BolsaEstudoCreate,
    BolsaEstudoEncerrar,
    BolsaEstudoResponse,
)
from apps.backend.app.modules.society.juventude.application.services.bolsa_estudo_service import (
    BolsaEstudoService,
)

router = APIRouter(prefix="/bolsas-estudo", tags=["Juventude - Bolsas Estudo"])

bolsa_estudo_service_dep = Depends(get_bolsa_estudo_service)


@router.post("/", response_model=BolsaEstudoResponse, status_code=status.HTTP_201_CREATED)
async def conceder_bolsa(
    data: BolsaEstudoCreate, service: BolsaEstudoService = bolsa_estudo_service_dep
) -> BolsaEstudoResponse:
    try:
        return await service.conceder_bolsa(
            jovem_id=data.jovem_id,
            tipo=data.tipo,
            valor_mensal=data.valor_mensal,
            data_inicio=data.data_inicio,
            data_fim=data.data_fim,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{bolsa_id}", response_model=BolsaEstudoResponse)
async def obter_bolsa(
    bolsa_id: UUID, service: BolsaEstudoService = bolsa_estudo_service_dep
) -> BolsaEstudoResponse:
    try:
        return await service.buscar_bolsa(bolsa_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[BolsaEstudoResponse])
async def listar_bolsas(
    jovem_id: UUID | None = None,
    apenas_ativas: bool | None = None,
    service: BolsaEstudoService = bolsa_estudo_service_dep,
) -> list[BolsaEstudoResponse]:
    return await service.listar_bolsas(jovem_id=jovem_id, apenas_ativas=apenas_ativas)


@router.patch("/{bolsa_id}/encerrar", response_model=BolsaEstudoResponse)
async def encerrar_bolsa(
    bolsa_id: UUID,
    data: BolsaEstudoEncerrar,
    service: BolsaEstudoService = bolsa_estudo_service_dep,
) -> BolsaEstudoResponse:
    try:
        return await service.encerrar_bolsa(bolsa_id=bolsa_id, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{bolsa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_bolsa(
    bolsa_id: UUID, service: BolsaEstudoService = bolsa_estudo_service_dep
) -> None:
    try:
        await service.remover_bolsa(bolsa_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc