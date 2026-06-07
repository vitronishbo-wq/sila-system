from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_tendencia_service
from apps.backend.app.modules.governance.statistics.api.schemas.tendencia_schema import (
    TendenciaCreate,
    TendenciaListResponse,
    TendenciaResponse,
    TendenciaUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.tendencia_service import (
    TendenciaService,
)
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

router = APIRouter(prefix="/tendencias", tags=["Estatistica - Tendencias"])

tendencia_service_dep = Depends(get_tendencia_service)
pagina_query = Query(1, ge=1)
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=TendenciaResponse, status_code=status.HTTP_201_CREATED)
async def criar_tendencia(
    data: TendenciaCreate, service: TendenciaService = tendencia_service_dep
) -> TendenciaResponse:
    return TendenciaResponse.model_validate(await service.criar(data.model_dump()))


@router.get("/", response_model=TendenciaListResponse)
async def listar_tendencias(
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: TendenciaService = tendencia_service_dep,
) -> TendenciaListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return TendenciaListResponse(
        itens=[TendenciaResponse.model_validate(i) for i in itens],
        total=len(itens),
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@router.get("/{tendencia_id}", response_model=TendenciaResponse)
async def obter_tendencia(
    tendencia_id: int, service: TendenciaService = tendencia_service_dep
) -> TendenciaResponse:
    try:
        return TendenciaResponse.model_validate(await service.obter(tendencia_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{tendencia_id}", response_model=TendenciaResponse)
async def atualizar_tendencia(
    tendencia_id: int,
    data: TendenciaUpdate,
    service: TendenciaService = tendencia_service_dep,
) -> TendenciaResponse:
    try:
        return TendenciaResponse.model_validate(
            await service.atualizar(tendencia_id, data.model_dump(exclude_unset=True))
        )
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{tendencia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tendencia(
    tendencia_id: int, service: TendenciaService = tendencia_service_dep
) -> None:
    try:
        await service.deletar(tendencia_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc