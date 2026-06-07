from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.resources.pescas.industrial.application.ports.produto_processado_repository_port import (
    ProdutoProcessadoRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.industrial.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.resources.pescas.industrial.application.ports.unidade_processamento_repository_port import (
    UnidadeProcessamentoRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import (
    MercadoDestino,
    TipoProcessamento,
    TipoProdutoProcessado,
)
from apps.backend.app.modules.resources.pescas.industrial.domain.models.produto_processado import (
    ProdutoProcessado,
)


class ProdutoProcessadoService:
    def __init__(
        self,
        *,
        produto_repo: ProdutoProcessadoRepositoryPort,
        unidade_repo: UnidadeProcessamentoRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.produto_repo = produto_repo
        self.unidade_repo = unidade_repo
        self.request_service = request_service

    async def cadastrar_produto(
        self,
        *,
        unidade_processamento_id: UUID,
        nome_comercial: str,
        tipo_produto: TipoProdutoProcessado,
        tipo_processamento: TipoProcessamento,
        peso_liquido_kg: Decimal,
        rendimento_percentual: Decimal,
        mercado_destino: MercadoDestino,
        observacoes: str | None = None,
    ) -> ProdutoProcessado:
        await self._validar_unidade(unidade_processamento_id)
        existentes = await self.produto_repo.list_by_unidade(unidade_processamento_id)
        normalized_name = nome_comercial.strip().lower()
        if any(
            item.nome_comercial.lower() == normalized_name and item.tipo_produto == tipo_produto
            for item in existentes
        ):
            raise ValueError("Produto ja cadastrado para a unidade com este nome e tipo")
        codigo = await self.produto_repo.next_codigo()
        produto = ProdutoProcessado.cadastrar(
            codigo_produto=codigo,
            unidade_processamento_id=unidade_processamento_id,
            nome_comercial=nome_comercial,
            tipo_produto=tipo_produto,
            tipo_processamento=tipo_processamento,
            peso_liquido_kg=peso_liquido_kg,
            rendimento_percentual=rendimento_percentual,
            mercado_destino=mercado_destino,
            observacoes=observacoes,
        )
        saved = await self.produto_repo.save(produto)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_PRODUTO_PROCESSADO",
                entity_id=saved.id,
                metadata={
                    "codigo_produto": saved.codigo_produto,
                    "tipo_produto": saved.tipo_produto.value,
                    "mercado_destino": saved.mercado_destino.value,
                },
                numero_processo=saved.codigo_produto,
            )
        return saved

    async def buscar_produto(self, produto_id: UUID) -> ProdutoProcessado:
        item = await self.produto_repo.get_by_id(produto_id)
        if not item:
            raise ValueError("Produto processado nao encontrado")
        return item

    async def listar_produtos(
        self,
        *,
        unidade_processamento_id: UUID | None = None,
        tipo_produto: TipoProdutoProcessado | None = None,
        mercado_destino: MercadoDestino | None = None,
        apenas_ativos: bool = True,
    ) -> list[ProdutoProcessado]:
        if unidade_processamento_id is not None:
            itens = await self.produto_repo.list_by_unidade(unidade_processamento_id)
        elif tipo_produto is not None:
            itens = await self.produto_repo.list_by_tipo(tipo_produto)
        elif mercado_destino is not None:
            itens = await self.produto_repo.list_by_destino(mercado_destino)
        else:
            itens = await self.produto_repo.list_all()
        if apenas_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_produto(
        self,
        *,
        produto_id: UUID,
        nome_comercial: str | None = None,
        tipo_produto: TipoProdutoProcessado | None = None,
        tipo_processamento: TipoProcessamento | None = None,
        peso_liquido_kg: Decimal | None = None,
        rendimento_percentual: Decimal | None = None,
        mercado_destino: MercadoDestino | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> ProdutoProcessado:
        item = await self.buscar_produto(produto_id)
        item.atualizar(
            nome_comercial=nome_comercial,
            tipo_produto=tipo_produto,
            tipo_processamento=tipo_processamento,
            peso_liquido_kg=peso_liquido_kg,
            rendimento_percentual=rendimento_percentual,
            mercado_destino=mercado_destino,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.produto_repo.save(item)

    async def remover_produto(self, produto_id: UUID) -> None:
        deleted = await self.produto_repo.delete(produto_id)
        if not deleted:
            raise ValueError("Produto processado nao encontrado")

    async def _validar_unidade(self, unidade_processamento_id: UUID) -> None:
        unidade = await self.unidade_repo.get_by_id(unidade_processamento_id)
        if unidade is None:
            raise ValueError("Unidade de processamento nao encontrada")
