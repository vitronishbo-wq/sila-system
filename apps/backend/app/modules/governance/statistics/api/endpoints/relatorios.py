from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_relatorio_service
from apps.backend.app.modules.governance.statistics.api.schemas.relatorio_schema import (
    RelatorioCreate,
    RelatorioListResponse,
    RelatorioResponse,
    RelatorioUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.relatorio_service import (
    RelatorioService,
)
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

router = APIRouter(prefix="/relatorios", tags=["Estatistica - Relatorios"])

relatorio_service_dep = Depends(get_relatorio_service)
pagina_query = Query(1, ge=1)
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=RelatorioResponse, status_code=status.HTTP_201_CREATED)
async def criar_relatorio(
    data: RelatorioCreate, service: RelatorioService = relatorio_service_dep
) -> RelatorioResponse:
    return RelatorioResponse.model_validate(await service.criar(data.model_dump()))


@router.get("/", response_model=RelatorioListResponse)
async def listar_relatorios(
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: RelatorioService = relatorio_service_dep,
) -> RelatorioListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return RelatorioListResponse(
        itens=[RelatorioResponse.model_validate(i) for i in itens],
        total=len(itens),
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@router.get("/{relatorio_id}", response_model=RelatorioResponse)
async def obter_relatorio(
    relatorio_id: int, service: RelatorioService = relatorio_service_dep
) -> RelatorioResponse:
    try:
        return RelatorioResponse.model_validate(await service.obter(relatorio_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{relatorio_id}", response_model=RelatorioResponse)
async def atualizar_relatorio(
    relatorio_id: int,
    data: RelatorioUpdate,
    service: RelatorioService = relatorio_service_dep,
) -> RelatorioResponse:
    try:
        return RelatorioResponse.model_validate(
            await service.atualizar(relatorio_id, data.model_dump(exclude_unset=True))
        )
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{relatorio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_relatorio(
    relatorio_id: int, service: RelatorioService = relatorio_service_dep
) -> None:
    try:
        await service.deletar(relatorio_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc