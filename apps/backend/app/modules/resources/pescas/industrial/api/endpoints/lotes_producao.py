from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.pescas.industrial.api.deps import get_lote_producao_service
from apps.backend.app.modules.resources.pescas.industrial.api.schemas.lote_producao_schema import (
    LoteProducaoCreate,
    LoteProducaoResponse,
    LoteProducaoUpdate,
)
from apps.backend.app.modules.resources.pescas.industrial.application.services.lote_producao_service import (
    LoteProducaoService,
)
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import StatusLoteProducao

router = APIRouter(prefix="/lotes-producao", tags=["Pescas Industriais - Lotes de Producao"])

lote_producao_service_dep = Depends(get_lote_producao_service)


@router.post("/", response_model=LoteProducaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_lote(
    data: LoteProducaoCreate, service: LoteProducaoService = lote_producao_service_dep
) -> LoteProducaoResponse:
    try:
        return await service.cadastrar_lote(
            unidade_processamento_id=data.unidade_processamento_id,
            produto_processado_id=data.produto_processado_id,
            data_producao=data.data_producao,
            quantidade_kg=data.quantidade_kg,
            destino_mercado=data.destino_mercado,
            data_validade=data.data_validade,
            turno=data.turno,
            temperatura_armazenamento_c=data.temperatura_armazenamento_c,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{lote_id}", response_model=LoteProducaoResponse)
async def obter_lote(
    lote_id: UUID, service: LoteProducaoService = lote_producao_service_dep
) -> LoteProducaoResponse:
    try:
        return await service.buscar_lote(lote_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[LoteProducaoResponse])
async def listar_lotes(
    unidade_processamento_id: UUID | None = None,
    produto_processado_id: UUID | None = None,
    status_lote: StatusLoteProducao | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    service: LoteProducaoService = lote_producao_service_dep,
) -> list[LoteProducaoResponse]:
    return await service.listar_lotes(
        unidade_processamento_id=unidade_processamento_id,
        produto_processado_id=produto_processado_id,
        status=status_lote,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


@router.patch("/{lote_id}", response_model=LoteProducaoResponse)
async def atualizar_lote(
    lote_id: UUID,
    data: LoteProducaoUpdate,
    service: LoteProducaoService = lote_producao_service_dep,
) -> LoteProducaoResponse:
    try:
        return await service.atualizar_lote(
            lote_id=lote_id,
            quantidade_kg=data.quantidade_kg,
            status=data.status,
            destino_mercado=data.destino_mercado,
            data_validade=data.data_validade,
            turno=data.turno,
            temperatura_armazenamento_c=data.temperatura_armazenamento_c,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        message = str(exc)
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in message.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=message) from exc


@router.delete("/{lote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_lote(
    lote_id: UUID, service: LoteProducaoService = lote_producao_service_dep
) -> None:
    try:
        await service.remover_lote(lote_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
