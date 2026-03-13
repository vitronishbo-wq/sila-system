from __future__ import annotations
import asyncio
from decimal import Decimal
import pytest
from app.modules.resources.pescas.industrial.application.services.produto_processado_service import ProdutoProcessadoService
from app.modules.resources.pescas.industrial.domain.enums import ClassificacaoIndustrial, MercadoDestino, TipoProcessamento, TipoProdutoProcessado
from app.modules.resources.pescas.industrial.domain.models.unidade_processamento import UnidadeProcessamento
from app.modules.resources.pescas.industrial.tests._fakes import InMemoryProdutoRepository, InMemoryUnidadeRepository

async def _seed_unidade(unidade_repo: InMemoryUnidadeRepository):
    unidade = UnidadeProcessamento.cadastrar(cnpj='12.345.678/0001-90', razao_social='Unidade Central', tipo_processamento=[TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_A, capacidade_kg_dia=Decimal('2500'), area_total_m2=Decimal('500'), area_producao_m2=Decimal('200'), area_armazenagem_m2=Decimal('120'), numero_funcionarios=18, endereco='Zona Industrial', municipio='Luanda', provincia='Luanda')
    return await unidade_repo.save(unidade)

def test_produto_crud_com_filtros() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadeRepository()
        produto_repo = InMemoryProdutoRepository()
        unidade = await _seed_unidade(unidade_repo)
        service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
        produto = await service.cadastrar_produto(unidade_processamento_id=unidade.id, nome_comercial='Filete Premium', tipo_produto=TipoProdutoProcessado.FILETE, tipo_processamento=TipoProcessamento.FILETAGEM, peso_liquido_kg=Decimal('1.5'), rendimento_percentual=Decimal('82'), mercado_destino=MercadoDestino.EXPORTACAO)
        assert produto.codigo_produto.startswith('PRD/')
        filtrados = await service.listar_produtos(tipo_produto=TipoProdutoProcessado.FILETE, apenas_ativos=True)
        assert len(filtrados) == 1
        atualizado = await service.atualizar_produto(produto_id=produto.id, ativo=False, observacoes='Descontinuado')
        assert atualizado.ativo is False
        ativos = await service.listar_produtos(apenas_ativos=True)
        assert ativos == []
    asyncio.run(scenario())

def test_produto_valida_duplicidade_mesma_unidade() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadeRepository()
        produto_repo = InMemoryProdutoRepository()
        unidade = await _seed_unidade(unidade_repo)
        service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
        await service.cadastrar_produto(unidade_processamento_id=unidade.id, nome_comercial='Conserva Azul', tipo_produto=TipoProdutoProcessado.CONSERVA, tipo_processamento=TipoProcessamento.CONSERVA, peso_liquido_kg=Decimal('0.4'), rendimento_percentual=Decimal('70'), mercado_destino=MercadoDestino.INTERNO)
        with pytest.raises(ValueError, match='ja cadastrado'):
            await service.cadastrar_produto(unidade_processamento_id=unidade.id, nome_comercial='Conserva Azul', tipo_produto=TipoProdutoProcessado.CONSERVA, tipo_processamento=TipoProcessamento.CONSERVA, peso_liquido_kg=Decimal('0.5'), rendimento_percentual=Decimal('72'), mercado_destino=MercadoDestino.INTERNO)
    asyncio.run(scenario())