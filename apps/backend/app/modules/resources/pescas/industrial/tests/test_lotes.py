from __future__ import annotations
import asyncio
from datetime import date
from decimal import Decimal
import pytest
from app.modules.resources.pescas.industrial.application.services.lote_producao_service import LoteProducaoService
from app.modules.resources.pescas.industrial.application.services.produto_processado_service import ProdutoProcessadoService
from app.modules.resources.pescas.industrial.domain.enums import ClassificacaoIndustrial, MercadoDestino, StatusLoteProducao, TipoProcessamento, TipoProdutoProcessado
from app.modules.resources.pescas.industrial.domain.models.unidade_processamento import UnidadeProcessamento
from app.modules.resources.pescas.industrial.tests._fakes import InMemoryLoteRepository, InMemoryProdutoRepository, InMemoryUnidadeRepository

async def _seed_unidade(unidade_repo: InMemoryUnidadeRepository, cnpj: str, nome: str):
    unidade = UnidadeProcessamento.cadastrar(cnpj=cnpj, razao_social=nome, tipo_processamento=[TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_A, capacidade_kg_dia=Decimal('3500'), area_total_m2=Decimal('650'), area_producao_m2=Decimal('230'), area_armazenagem_m2=Decimal('180'), numero_funcionarios=25, endereco='Zona Industrial', municipio='Benguela', provincia='Benguela')
    return await unidade_repo.save(unidade)

def test_lote_crud_com_filtros() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadeRepository()
        produto_repo = InMemoryProdutoRepository()
        lote_repo = InMemoryLoteRepository()
        unidade = await _seed_unidade(unidade_repo, '22.345.678/0001-90', 'Unidade Sul')
        produto_service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
        lote_service = LoteProducaoService(lote_repo=lote_repo, produto_repo=produto_repo, unidade_repo=unidade_repo)
        produto = await produto_service.cadastrar_produto(unidade_processamento_id=unidade.id, nome_comercial='Atum Congelado', tipo_produto=TipoProdutoProcessado.CONGELADO, tipo_processamento=TipoProcessamento.CONGELADO, peso_liquido_kg=Decimal('2.0'), rendimento_percentual=Decimal('77'), mercado_destino=MercadoDestino.EXPORTACAO)
        lote = await lote_service.cadastrar_lote(unidade_processamento_id=unidade.id, produto_processado_id=produto.id, data_producao=date(2026, 2, 15), quantidade_kg=Decimal('1200'), destino_mercado=MercadoDestino.EXPORTACAO)
        assert lote.codigo_lote.startswith('LOT/')
        assert lote.status == StatusLoteProducao.ABERTO
        atualizado = await lote_service.atualizar_lote(lote_id=lote.id, status=StatusLoteProducao.CONCLUIDO, observacoes='Processamento finalizado')
        assert atualizado.status == StatusLoteProducao.CONCLUIDO
        concluidos = await lote_service.listar_lotes(status=StatusLoteProducao.CONCLUIDO)
        assert len(concluidos) == 1
    asyncio.run(scenario())

def test_lote_rejeita_produto_de_outra_unidade() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadeRepository()
        produto_repo = InMemoryProdutoRepository()
        lote_repo = InMemoryLoteRepository()
        unidade_a = await _seed_unidade(unidade_repo, '32.345.678/0001-90', 'Unidade A')
        unidade_b = await _seed_unidade(unidade_repo, '42.345.678/0001-90', 'Unidade B')
        produto_service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
        lote_service = LoteProducaoService(lote_repo=lote_repo, produto_repo=produto_repo, unidade_repo=unidade_repo)
        produto = await produto_service.cadastrar_produto(unidade_processamento_id=unidade_a.id, nome_comercial='Pescada Seca', tipo_produto=TipoProdutoProcessado.SECO, tipo_processamento=TipoProcessamento.SECO, peso_liquido_kg=Decimal('1.0'), rendimento_percentual=Decimal('62'), mercado_destino=MercadoDestino.INTERNO)
        with pytest.raises(ValueError, match='nao pertence'):
            await lote_service.cadastrar_lote(unidade_processamento_id=unidade_b.id, produto_processado_id=produto.id, data_producao=date(2026, 2, 20), quantidade_kg=Decimal('300'), destino_mercado=MercadoDestino.INTERNO)
    asyncio.run(scenario())