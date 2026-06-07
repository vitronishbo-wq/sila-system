from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_comparativo_service
from apps.backend.app.modules.governance.statistics.api.schemas.comparativo_schema import (
    ComparativoCreate,
    ComparativoListResponse,
    ComparativoResponse,
    ComparativoUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.comparativo_service import (
    ComparativoService,
)
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

router = APIRouter(prefix="/comparativos", tags=["Estatistica - Comparativos"])

comparativo_service_dep = Depends(get_comparativo_service)
pagina_query = Query(1, ge=1)
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=ComparativoResponse, status_code=status.HTTP_201_CREATED)
async def criar_comparativo(
    data: ComparativoCreate, service: ComparativoService = comparativo_service_dep
) -> ComparativoResponse:
    return ComparativoResponse.model_validate(await service.criar(data.model_dump()))


@router.get("/", response_model=ComparativoListResponse)
async def listar_comparativos(
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: ComparativoService = comparativo_service_dep,
) -> ComparativoListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return ComparativoListResponse(
        itens=[ComparativoResponse.model_validate(i) for i in itens],
        total=len(itens),
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@router.get("/{comparativo_id}", response_model=ComparativoResponse)
async def obter_comparativo(
    comparativo_id: int, service: ComparativoService = comparativo_service_dep
) -> ComparativoResponse:
    try:
        return ComparativoResponse.model_validate(await service.obter(comparativo_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{comparativo_id}", response_model=ComparativoResponse)
async def atualizar_comparativo(
    comparativo_id: int,
    data: ComparativoUpdate,
    service: ComparativoService = comparativo_service_dep,
) -> ComparativoResponse:
    try:
        return ComparativoResponse.model_validate(
            await service.atualizar(comparativo_id, data.model_dump(exclude_unset=True))
        )
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{comparativo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_comparativo(
    comparativo_id: int, service: ComparativoService = comparativo_service_dep
) -> None:
    try:
        await service.deletar(comparativo_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc