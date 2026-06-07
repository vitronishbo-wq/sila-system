from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_kpi_service
from apps.backend.app.modules.governance.statistics.api.schemas.kpi_schema import (
    KPICreate,
    KPIListaResponse,
    KPIResponse,
    KPIUpdate,
    KPIValorUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.kpi_service import (
    KPIService,
)
from apps.backend.app.modules.governance.statistics.domain.enums import StatusKPI
from apps.backend.app.modules.governance.statistics.exceptions import (
    EstatisticaConflictError,
    EstatisticaNotFoundError,
)

router = APIRouter(prefix="/kpis", tags=["Estatistica - KPIs"])

kpi_service_dep = Depends(get_kpi_service)
limit_query = Query(50, ge=1, le=200)
pagina_query = Query(1, ge=1)
status_kpi_query = Query(None, alias="status")
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=KPIResponse, status_code=status.HTTP_201_CREATED)
async def criar_kpi(data: KPICreate, service: KPIService = kpi_service_dep) -> KPIResponse:
    try:
        return KPIResponse.model_validate(await service.criar_kpi(data.model_dump()))
    except EstatisticaConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/status/criticos", response_model=list[KPIResponse])
async def listar_kpis_criticos(
    limit: int = limit_query, service: KPIService = kpi_service_dep
) -> list[KPIResponse]:
    return [KPIResponse.model_validate(k) for k in await service.get_kpis_criticos(limit)]


@router.get("/", response_model=KPIListaResponse)
async def listar_kpis(
    status_kpi: StatusKPI | None = status_kpi_query,
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: KPIService = kpi_service_dep,
) -> KPIListaResponse:
    offset = (pagina - 1) * tamanho_pagina
    kpis = await service.listar_kpis(status=status_kpi, limit=tamanho_pagina, offset=offset)
    return KPIListaResponse(
        kpis=[KPIResponse.model_validate(k) for k in kpis],
        total=len(kpis),
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
        filtros_aplicados={"status": status_kpi.value if status_kpi else None},
    )


@router.get("/{kpi_id}", response_model=KPIResponse)
async def obter_kpi(kpi_id: int, service: KPIService = kpi_service_dep) -> KPIResponse:
    try:
        return KPIResponse.model_validate(await service.obter_kpi(kpi_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{kpi_id}/performance", response_model=dict)
async def calcular_performance_kpi(
    kpi_id: int, service: KPIService = kpi_service_dep
) -> dict:
    try:
        return await service.calcular_performance_kpi(kpi_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{kpi_id}", response_model=KPIResponse)
async def atualizar_kpi(
    kpi_id: int, data: KPIUpdate, service: KPIService = kpi_service_dep
) -> KPIResponse:
    try:
        updated = await service.atualizar_kpi(kpi_id, data.model_dump(exclude_unset=True))
        return KPIResponse.model_validate(updated)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{kpi_id}/valor", response_model=KPIResponse)
async def atualizar_valor_kpi(
    kpi_id: int, data: KPIValorUpdate, service: KPIService = kpi_service_dep
) -> KPIResponse:
    try:
        updated = await service.atualizar_valor_kpi(kpi_id, data.valor)
        return KPIResponse.model_validate(updated)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{kpi_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_kpi(kpi_id: int, service: KPIService = kpi_service_dep) -> None:
    try:
        await service.deletar_kpi(kpi_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
