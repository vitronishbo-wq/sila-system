from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.pescas.industrial.api.deps import (
    get_produto_processado_service,
)
from apps.backend.app.modules.resources.pescas.industrial.api.schemas.produto_processado_schema import (
    ProdutoProcessadoCreate,
    ProdutoProcessadoResponse,
    ProdutoProcessadoUpdate,
)
from apps.backend.app.modules.resources.pescas.industrial.application.services.produto_processado_service import (
    ProdutoProcessadoService,
)
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import (
    MercadoDestino,
    TipoProdutoProcessado,
)

router = APIRouter(
    prefix="/produtos-processados", tags=["Pescas Industriais - Produtos Processados"]
)

produto_processado_service_dep = Depends(get_produto_processado_service)


@router.post("/", response_model=ProdutoProcessadoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_produto(
    data: ProdutoProcessadoCreate,
    service: ProdutoProcessadoService = produto_processado_service_dep,
) -> ProdutoProcessadoResponse:
    try:
        return await service.cadastrar_produto(
            unidade_processamento_id=data.unidade_processamento_id,
            nome_comercial=data.nome_comercial,
            tipo_produto=data.tipo_produto,
            tipo_processamento=data.tipo_processamento,
            peso_liquido_kg=data.peso_liquido_kg,
            rendimento_percentual=data.rendimento_percentual,
            mercado_destino=data.mercado_destino,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{produto_id}", response_model=ProdutoProcessadoResponse)
async def obter_produto(
    produto_id: UUID, service: ProdutoProcessadoService = produto_processado_service_dep
) -> ProdutoProcessadoResponse:
    try:
        return await service.buscar_produto(produto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ProdutoProcessadoResponse])
async def listar_produtos(
    unidade_processamento_id: UUID | None = None,
    tipo_produto: TipoProdutoProcessado | None = None,
    mercado_destino: MercadoDestino | None = None,
    apenas_ativos: bool = True,
    service: ProdutoProcessadoService = produto_processado_service_dep,
) -> list[ProdutoProcessadoResponse]:
    return await service.listar_produtos(
        unidade_processamento_id=unidade_processamento_id,
        tipo_produto=tipo_produto,
        mercado_destino=mercado_destino,
        apenas_ativos=apenas_ativos,
    )


@router.patch("/{produto_id}", response_model=ProdutoProcessadoResponse)
async def atualizar_produto(
    produto_id: UUID,
    data: ProdutoProcessadoUpdate,
    service: ProdutoProcessadoService = produto_processado_service_dep,
) -> ProdutoProcessadoResponse:
    try:
        return await service.atualizar_produto(
            produto_id=produto_id,
            nome_comercial=data.nome_comercial,
            tipo_produto=data.tipo_produto,
            tipo_processamento=data.tipo_processamento,
            peso_liquido_kg=data.peso_liquido_kg,
            rendimento_percentual=data.rendimento_percentual,
            mercado_destino=data.mercado_destino,
            ativo=data.ativo,
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


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_produto(
    produto_id: UUID, service: ProdutoProcessadoService = produto_processado_service_dep
) -> None:
    try:
        await service.remover_produto(produto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
