from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_indicador_service
from apps.backend.app.modules.governance.statistics.api.schemas.indicador_schema import (
    IndicadorCreate,
    IndicadorListResponse,
    IndicadorResponse,
    IndicadorUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.indicador_service import (
    IndicadorService,
)
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

router = APIRouter(prefix="/indicadores", tags=["Estatistica - Indicadores"])

indicador_service_dep = Depends(get_indicador_service)
pagina_query = Query(1, ge=1)
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=IndicadorResponse, status_code=status.HTTP_201_CREATED)
async def criar_indicador(
    data: IndicadorCreate, service: IndicadorService = indicador_service_dep
) -> IndicadorResponse:
    return IndicadorResponse.model_validate(await service.criar(data.model_dump()))


@router.get("/", response_model=IndicadorListResponse)
async def listar_indicadores(
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: IndicadorService = indicador_service_dep,
) -> IndicadorListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return IndicadorListResponse(
        itens=[IndicadorResponse.model_validate(i) for i in itens],
        total=len(itens),
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@router.get("/{indicador_id}", response_model=IndicadorResponse)
async def obter_indicador(
    indicador_id: int, service: IndicadorService = indicador_service_dep
) -> IndicadorResponse:
    try:
        return IndicadorResponse.model_validate(await service.obter(indicador_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{indicador_id}", response_model=IndicadorResponse)
async def atualizar_indicador(
    indicador_id: int,
    data: IndicadorUpdate,
    service: IndicadorService = indicador_service_dep,
) -> IndicadorResponse:
    try:
        return IndicadorResponse.model_validate(
            await service.atualizar(indicador_id, data.model_dump(exclude_unset=True))
        )
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{indicador_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_indicador(
    indicador_id: int, service: IndicadorService = indicador_service_dep
) -> None:
    try:
        await service.deletar(indicador_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc