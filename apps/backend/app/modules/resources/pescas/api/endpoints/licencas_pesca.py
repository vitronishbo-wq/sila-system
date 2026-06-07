from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.pescas.api.deps import get_licenciamento_pesca_service
from apps.backend.app.modules.resources.pescas.api.schemas.licenca_pesca_schema import (
    LicencaPescaCreate,
    LicencaPescaResponse,
)
from apps.backend.app.modules.resources.pescas.application.services.licenciamento_pesca_service import (
    LicenciamentoPescaService,
)

router = APIRouter(prefix="/licencas-pesca", tags=["Pescas - Licencas"])

licenciamento_pesca_service_dep = Depends(get_licenciamento_pesca_service)


@router.post("/", response_model=LicencaPescaResponse, status_code=status.HTTP_201_CREATED)
async def emitir_licenca(
    data: LicencaPescaCreate,
    service: LicenciamentoPescaService = licenciamento_pesca_service_dep,
):
    try:
        return await service.emitir_licenca(
            embarcacao_id=data.embarcacao_id,
            titular_id=data.titular_id,
            modalidade_autorizada=data.modalidade_autorizada,
            zona_pesca_id=data.zona_pesca_id,
            validade_dias=data.validade_dias,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{licenca_id}", response_model=LicencaPescaResponse)
async def obter_licenca(
    licenca_id: UUID, service: LicenciamentoPescaService = licenciamento_pesca_service_dep
):
    try:
        return await service.buscar_licenca(licenca_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[LicencaPescaResponse])
async def listar_licencas_validas(
    service: LicenciamentoPescaService = licenciamento_pesca_service_dep,
):
    return await service.listar_licencas_validas()