from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.resources.pescas.industrial.application.ports.lote_producao_repository_port import LoteProducaoRepositoryPort
from app.modules.resources.pescas.industrial.application.ports.produto_processado_repository_port import ProdutoProcessadoRepositoryPort
from app.modules.resources.pescas.industrial.application.ports.request_service_port import RequestServicePort
from app.modules.resources.pescas.industrial.application.ports.unidade_processamento_repository_port import UnidadeProcessamentoRepositoryPort
from app.modules.resources.pescas.industrial.domain.enums import MercadoDestino, StatusLoteProducao
from app.modules.resources.pescas.industrial.domain.models.lote_producao import LoteProducao

class LoteProducaoService:

    def __init__(self, *, lote_repo: LoteProducaoRepositoryPort, produto_repo: ProdutoProcessadoRepositoryPort, unidade_repo: UnidadeProcessamentoRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.lote_repo = lote_repo
        self.produto_repo = produto_repo
        self.unidade_repo = unidade_repo
        self.request_service = request_service

    async def cadastrar_lote(self, *, unidade_processamento_id: UUID, produto_processado_id: UUID, data_producao: date, quantidade_kg: Decimal, destino_mercado: MercadoDestino, data_validade: date | None=None, turno: str | None=None, temperatura_armazenamento_c: Decimal | None=None, observacoes: str | None=None) -> LoteProducao:
        await self._validar_unidade(unidade_processamento_id)
        produto = await self._validar_produto(produto_processado_id)
        if produto.unidade_processamento_id != unidade_processamento_id:
            raise ValueError('Produto nao pertence a unidade informada')
        codigo = await self.lote_repo.next_codigo()
        lote = LoteProducao.criar(codigo_lote=codigo, unidade_processamento_id=unidade_processamento_id, produto_processado_id=produto_processado_id, data_producao=data_producao, quantidade_kg=quantidade_kg, destino_mercado=destino_mercado, data_validade=data_validade, turno=turno, temperatura_armazenamento_c=temperatura_armazenamento_c, observacoes=observacoes)
        saved = await self.lote_repo.save(lote)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='ABERTURA_LOTE_PRODUCAO', entity_id=saved.id, metadata={'codigo_lote': saved.codigo_lote, 'produto_id': str(saved.produto_processado_id), 'quantidade_kg': str(saved.quantidade_kg)}, numero_processo=saved.codigo_lote)
        return saved

    async def buscar_lote(self, lote_id: UUID) -> LoteProducao:
        item = await self.lote_repo.get_by_id(lote_id)
        if not item:
            raise ValueError('Lote de producao nao encontrado')
        return item

    async def listar_lotes(self, *, unidade_processamento_id: UUID | None=None, produto_processado_id: UUID | None=None, status: StatusLoteProducao | None=None, data_inicio: date | None=None, data_fim: date | None=None) -> list[LoteProducao]:
        if unidade_processamento_id is not None:
            return await self.lote_repo.list_by_unidade(unidade_processamento_id)
        if produto_processado_id is not None:
            return await self.lote_repo.list_by_produto(produto_processado_id)
        if status is not None:
            return await self.lote_repo.list_by_status(status)
        if data_inicio is not None and data_fim is not None:
            return await self.lote_repo.list_by_periodo(data_inicio, data_fim)
        return await self.lote_repo.list_all()

    async def atualizar_lote(self, *, lote_id: UUID, quantidade_kg: Decimal | None=None, status: StatusLoteProducao | None=None, destino_mercado: MercadoDestino | None=None, data_validade: date | None=None, turno: str | None=None, temperatura_armazenamento_c: Decimal | None=None, observacoes: str | None=None) -> LoteProducao:
        item = await self.buscar_lote(lote_id)
        item.atualizar(quantidade_kg=quantidade_kg, status=status, destino_mercado=destino_mercado, data_validade=data_validade, turno=turno, temperatura_armazenamento_c=temperatura_armazenamento_c, observacoes=observacoes)
        return await self.lote_repo.save(item)

    async def remover_lote(self, lote_id: UUID) -> None:
        deleted = await self.lote_repo.delete(lote_id)
        if not deleted:
            raise ValueError('Lote de producao nao encontrado')

    async def _validar_unidade(self, unidade_processamento_id: UUID) -> None:
        unidade = await self.unidade_repo.get_by_id(unidade_processamento_id)
        if unidade is None:
            raise ValueError('Unidade de processamento nao encontrada')

    async def _validar_produto(self, produto_processado_id: UUID):
        produto = await self.produto_repo.get_by_id(produto_processado_id)
        if produto is None:
            raise ValueError('Produto processado nao encontrado')
        return produto