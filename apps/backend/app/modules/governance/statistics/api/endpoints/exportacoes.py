from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_exportacao_service
from apps.backend.app.modules.governance.statistics.api.schemas.exportacao_schema import (
    ExportacaoCreate,
    ExportacaoListResponse,
    ExportacaoResponse,
    ExportacaoUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.exportacao_service import (
    ExportacaoService,
)
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

router = APIRouter(prefix="/exportacoes", tags=["Estatistica - Exportacoes"])

exportacao_service_dep = Depends(get_exportacao_service)
pagina_query = Query(1, ge=1)
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=ExportacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_exportacao(
    data: ExportacaoCreate, service: ExportacaoService = exportacao_service_dep
) -> ExportacaoResponse:
    return ExportacaoResponse.model_validate(await service.criar(data.model_dump()))


@router.get("/", response_model=ExportacaoListResponse)
async def listar_exportacoes(
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: ExportacaoService = exportacao_service_dep,
) -> ExportacaoListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return ExportacaoListResponse(
        itens=[ExportacaoResponse.model_validate(i) for i in itens],
        total=len(itens),
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@router.get("/{exportacao_id}", response_model=ExportacaoResponse)
async def obter_exportacao(
    exportacao_id: int, service: ExportacaoService = exportacao_service_dep
) -> ExportacaoResponse:
    try:
        return ExportacaoResponse.model_validate(await service.obter(exportacao_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{exportacao_id}", response_model=ExportacaoResponse)
async def atualizar_exportacao(
    exportacao_id: int,
    data: ExportacaoUpdate,
    service: ExportacaoService = exportacao_service_dep,
) -> ExportacaoResponse:
    try:
        return ExportacaoResponse.model_validate(
            await service.atualizar(exportacao_id, data.model_dump(exclude_unset=True))
        )
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{exportacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_exportacao(
    exportacao_id: int, service: ExportacaoService = exportacao_service_dep
) -> None:
    try:
        await service.deletar(exportacao_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc