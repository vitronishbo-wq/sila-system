from __future__ import annotations
import asyncio
from datetime import date
from decimal import Decimal
import pytest
from apps.backend.app.modules.resources.pescas.industrial.application.services.inspecao_industrial_service import InspecaoIndustrialService
from apps.backend.app.modules.resources.pescas.industrial.application.services.lote_producao_service import LoteProducaoService
from apps.backend.app.modules.resources.pescas.industrial.application.services.produto_processado_service import ProdutoProcessadoService
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import ClassificacaoIndustrial, MercadoDestino, StatusInspecao, TipoProcessamento, TipoProdutoProcessado, TipoSeloInspecao
from apps.backend.app.modules.resources.pescas.industrial.domain.models.unidade_processamento import UnidadeProcessamento
from apps.backend.app.modules.resources.pescas.industrial.tests._fakes import InMemoryInspecaoRepository, InMemoryLoteRepository, InMemoryProdutoRepository, InMemoryUnidadeRepository

async def _seed_unidade(unidade_repo: InMemoryUnidadeRepository, cnpj: str, nome: str):
    unidade = UnidadeProcessamento.cadastrar(cnpj=cnpj, razao_social=nome, tipo_processamento=[TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_B, capacidade_kg_dia=Decimal('2100'), area_total_m2=Decimal('420'), area_producao_m2=Decimal('180'), area_armazenagem_m2=Decimal('130'), numero_funcionarios=16, endereco='Zona Portuaria', municipio='Namibe', provincia='Namibe')
    return await unidade_repo.save(unidade)

def test_inspecao_fluxo_status_completo() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadeRepository()
        produto_repo = InMemoryProdutoRepository()
        lote_repo = InMemoryLoteRepository()
        inspecao_repo = InMemoryInspecaoRepository()
        unidade = await _seed_unidade(unidade_repo, '52.345.678/0001-90', 'Unidade Porto')
        produto_service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
        lote_service = LoteProducaoService(lote_repo=lote_repo, produto_repo=produto_repo, unidade_repo=unidade_repo)
        inspecao_service = InspecaoIndustrialService(inspecao_repo=inspecao_repo, unidade_repo=unidade_repo, lote_repo=lote_repo)
        produto = await produto_service.cadastrar_produto(unidade_processamento_id=unidade.id, nome_comercial='Filete Branco', tipo_produto=TipoProdutoProcessado.FILETE, tipo_processamento=TipoProcessamento.FILETAGEM, peso_liquido_kg=Decimal('1.2'), rendimento_percentual=Decimal('80'), mercado_destino=MercadoDestino.INTERNO)
        lote = await lote_service.cadastrar_lote(unidade_processamento_id=unidade.id, produto_processado_id=produto.id, data_producao=date(2026, 2, 18), quantidade_kg=Decimal('700'), destino_mercado=MercadoDestino.INTERNO)
        inspecao = await inspecao_service.agendar_inspecao(unidade_processamento_id=unidade.id, data_agendada=date(2026, 2, 19), selo_inspecao=TipoSeloInspecao.SIF, lote_producao_id=lote.id)
        assert inspecao.status == StatusInspecao.AGENDADA
        em_andamento = await inspecao_service.atualizar_status(inspecao_id=inspecao.id, status=StatusInspecao.EM_ANDAMENTO)
        assert em_andamento.status == StatusInspecao.EM_ANDAMENTO
        aprovada = await inspecao_service.atualizar_status(inspecao_id=inspecao.id, status=StatusInspecao.APROVADA, pontuacao=96, aprovada=True)
        assert aprovada.status == StatusInspecao.APROVADA
        aprovadas = await inspecao_service.listar_inspecoes(status=StatusInspecao.APROVADA)
        assert len(aprovadas) == 1
    asyncio.run(scenario())

def test_inspecao_rejeita_lote_de_outra_unidade() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadeRepository()
        lote_repo = InMemoryLoteRepository()
        inspecao_repo = InMemoryInspecaoRepository()
        produto_repo = InMemoryProdutoRepository()
        unidade_a = await _seed_unidade(unidade_repo, '62.345.678/0001-90', 'Unidade A')
        unidade_b = await _seed_unidade(unidade_repo, '72.345.678/0001-90', 'Unidade B')
        produto_service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
        lote_service = LoteProducaoService(lote_repo=lote_repo, produto_repo=produto_repo, unidade_repo=unidade_repo)
        inspecao_service = InspecaoIndustrialService(inspecao_repo=inspecao_repo, unidade_repo=unidade_repo, lote_repo=lote_repo)
        produto = await produto_service.cadastrar_produto(unidade_processamento_id=unidade_a.id, nome_comercial='Conserva Clara', tipo_produto=TipoProdutoProcessado.CONSERVA, tipo_processamento=TipoProcessamento.CONSERVA, peso_liquido_kg=Decimal('0.6'), rendimento_percentual=Decimal('73'), mercado_destino=MercadoDestino.INTERNO)
        lote = await lote_service.cadastrar_lote(unidade_processamento_id=unidade_a.id, produto_processado_id=produto.id, data_producao=date(2026, 2, 25), quantidade_kg=Decimal('310'), destino_mercado=MercadoDestino.INTERNO)
        with pytest.raises(ValueError, match='nao pertence'):
            await inspecao_service.agendar_inspecao(unidade_processamento_id=unidade_b.id, data_agendada=date(2026, 2, 26), selo_inspecao=TipoSeloInspecao.SIE, lote_producao_id=lote.id)
    asyncio.run(scenario())