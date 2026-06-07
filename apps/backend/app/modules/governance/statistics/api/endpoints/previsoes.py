from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_previsao_service
from apps.backend.app.modules.governance.statistics.api.schemas.previsao_schema import (
    PrevisaoCreate,
    PrevisaoListResponse,
    PrevisaoResponse,
    PrevisaoUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.previsao_service import (
    PrevisaoService,
)
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

router = APIRouter(prefix="/previsoes", tags=["Estatistica - Previsoes"])

previsao_service_dep = Depends(get_previsao_service)
pagina_query = Query(1, ge=1)
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=PrevisaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_previsao(
    data: PrevisaoCreate, service: PrevisaoService = previsao_service_dep
) -> PrevisaoResponse:
    return PrevisaoResponse.model_validate(await service.criar(data.model_dump()))


@router.get("/", response_model=PrevisaoListResponse)
async def listar_previsoes(
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: PrevisaoService = previsao_service_dep,
) -> PrevisaoListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return PrevisaoListResponse(
        itens=[PrevisaoResponse.model_validate(i) for i in itens],
        total=len(itens),
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@router.get("/{previsao_id}", response_model=PrevisaoResponse)
async def obter_previsao(
    previsao_id: int, service: PrevisaoService = previsao_service_dep
) -> PrevisaoResponse:
    try:
        return PrevisaoResponse.model_validate(await service.obter(previsao_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{previsao_id}", response_model=PrevisaoResponse)
async def atualizar_previsao(
    previsao_id: int, data: PrevisaoUpdate, service: PrevisaoService = previsao_service_dep
) -> PrevisaoResponse:
    try:
        return PrevisaoResponse.model_validate(
            await service.atualizar(previsao_id, data.model_dump(exclude_unset=True))
        )
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{previsao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_previsao(
    previsao_id: int, service: PrevisaoService = previsao_service_dep
) -> None:
    try:
        await service.deletar(previsao_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc