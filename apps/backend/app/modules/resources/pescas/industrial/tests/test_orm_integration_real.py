from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from datetime import date
from decimal import Decimal
from uuid import uuid4
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.domain.db import AsyncSessionLocal, Base, engine
from apps.backend.app.modules.resources.pescas.industrial.application.services.inspecao_industrial_service import InspecaoIndustrialService
from apps.backend.app.modules.resources.pescas.industrial.application.services.lote_producao_service import LoteProducaoService
from apps.backend.app.modules.resources.pescas.industrial.application.services.produto_processado_service import ProdutoProcessadoService
from apps.backend.app.modules.resources.pescas.industrial.application.services.unidade_processamento_service import UnidadeProcessamentoService
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import ClassificacaoIndustrial, MercadoDestino, StatusInspecao, StatusLoteProducao, TipoProcessamento, TipoProdutoProcessado, TipoSeloInspecao
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.inspecao_model import InspecaoModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.lote_producao_model import LoteProducaoModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.produto_processado_model import ProdutoProcessadoModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.unidade_processamento_model import UnidadeProcessamentoModel
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_inspecao_repository import SQLAlchemyInspecaoRepository
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_lote_producao_repository import SQLAlchemyLoteProducaoRepository
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_produto_processado_repository import SQLAlchemyProdutoProcessadoRepository
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_unidade_processamento_repository import SQLAlchemyUnidadeProcessamentoRepository
_TABLES = [UnidadeProcessamentoModel.__table__, ProdutoProcessadoModel.__table__, LoteProducaoModel.__table__, InspecaoModel.__table__]

class _FakePescasService:

    async def armador_exists(self, armador_id):
        return True

class _FakeIndustriaService:

    async def cnpj_ativo(self, cnpj: str) -> bool:
        return True

async def _ensure_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=_TABLES))

async def _clear_data(session: AsyncSession) -> None:
    await session.execute(text('DELETE FROM pescas_industriais_inspecoes'))
    await session.execute(text('DELETE FROM pescas_industriais_lotes_producao'))
    await session.execute(text('DELETE FROM pescas_industriais_produtos_processados'))
    await session.execute(text('DELETE FROM pescas_industriais_unidades'))
    await session.commit()

@asynccontextmanager
async def _session_scope():
    await _ensure_schema()
    async with AsyncSessionLocal() as session:
        await _clear_data(session)
        try:
            yield session
        finally:
            await _clear_data(session)

@pytest.mark.integration
def test_fluxo_real_orm_unidade_produto_lote_inspecao() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            unidade_repo = SQLAlchemyUnidadeProcessamentoRepository(session)
            produto_repo = SQLAlchemyProdutoProcessadoRepository(session)
            lote_repo = SQLAlchemyLoteProducaoRepository(session)
            inspecao_repo = SQLAlchemyInspecaoRepository(session)
            unidade_service = UnidadeProcessamentoService(unidade_repo=unidade_repo, pescas_service=_FakePescasService(), industria_service=_FakeIndustriaService())
            produto_service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
            lote_service = LoteProducaoService(lote_repo=lote_repo, produto_repo=produto_repo, unidade_repo=unidade_repo)
            inspecao_service = InspecaoIndustrialService(inspecao_repo=inspecao_repo, unidade_repo=unidade_repo, lote_repo=lote_repo)
            unidade = await unidade_service.cadastrar_unidade(cnpj='91.111.111/0001-11', razao_social='Unidade Integracao', tipo_processamento=[TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_A, capacidade_kg_dia=Decimal('5000'), area_total_m2=Decimal('900'), area_producao_m2=Decimal('350'), area_armazenagem_m2=Decimal('280'), numero_funcionarios=42, endereco='Zona Portuaria 1', municipio='Luanda', provincia='Luanda', armador_id=uuid4())
            produto = await produto_service.cadastrar_produto(unidade_processamento_id=unidade.id, nome_comercial='Filete Real', tipo_produto=TipoProdutoProcessado.FILETE, tipo_processamento=TipoProcessamento.FILETAGEM, peso_liquido_kg=Decimal('1.1'), rendimento_percentual=Decimal('79'), mercado_destino=MercadoDestino.EXPORTACAO)
            lote = await lote_service.cadastrar_lote(unidade_processamento_id=unidade.id, produto_processado_id=produto.id, data_producao=date(2026, 3, 2), quantidade_kg=Decimal('1200'), destino_mercado=MercadoDestino.EXPORTACAO)
            inspecao = await inspecao_service.agendar_inspecao(unidade_processamento_id=unidade.id, data_agendada=date(2026, 3, 3), selo_inspecao=TipoSeloInspecao.SIF, lote_producao_id=lote.id)
            lote_atualizado = await lote_service.atualizar_lote(lote_id=lote.id, status=StatusLoteProducao.CONCLUIDO)
            inspecao_aprovada = await inspecao_service.atualizar_status(inspecao_id=inspecao.id, status=StatusInspecao.APROVADA, pontuacao=95, aprovada=True)
            assert produto.codigo_produto.startswith('PRD/')
            assert lote.codigo_lote.startswith('LOT/')
            assert inspecao.codigo_inspecao.startswith('INS/')
            assert lote_atualizado.status == StatusLoteProducao.CONCLUIDO
            assert inspecao_aprovada.status == StatusInspecao.APROVADA
    asyncio.run(scenario())

@pytest.mark.integration
def test_integracao_real_lote_valida_produto_unidade() -> None:

    async def scenario() -> None:
        async with _session_scope() as session:
            unidade_repo = SQLAlchemyUnidadeProcessamentoRepository(session)
            produto_repo = SQLAlchemyProdutoProcessadoRepository(session)
            lote_repo = SQLAlchemyLoteProducaoRepository(session)
            unidade_service = UnidadeProcessamentoService(unidade_repo=unidade_repo, pescas_service=_FakePescasService(), industria_service=_FakeIndustriaService())
            produto_service = ProdutoProcessadoService(produto_repo=produto_repo, unidade_repo=unidade_repo)
            lote_service = LoteProducaoService(lote_repo=lote_repo, produto_repo=produto_repo, unidade_repo=unidade_repo)
            unidade_a = await unidade_service.cadastrar_unidade(cnpj='91.222.222/0001-22', razao_social='Unidade A', tipo_processamento=[TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_B, capacidade_kg_dia=Decimal('3000'), area_total_m2=Decimal('700'), area_producao_m2=Decimal('300'), area_armazenagem_m2=Decimal('220'), numero_funcionarios=30, endereco='Zona A', municipio='Benguela', provincia='Benguela')
            unidade_b = await unidade_service.cadastrar_unidade(cnpj='91.333.333/0001-33', razao_social='Unidade B', tipo_processamento=[TipoProcessamento.CONGELADO], classificacao=ClassificacaoIndustrial.TIPO_C, capacidade_kg_dia=Decimal('3200'), area_total_m2=Decimal('710'), area_producao_m2=Decimal('310'), area_armazenagem_m2=Decimal('230'), numero_funcionarios=31, endereco='Zona B', municipio='Benguela', provincia='Benguela')
            produto = await produto_service.cadastrar_produto(unidade_processamento_id=unidade_a.id, nome_comercial='Produto A', tipo_produto=TipoProdutoProcessado.CONGELADO, tipo_processamento=TipoProcessamento.CONGELADO, peso_liquido_kg=Decimal('2.3'), rendimento_percentual=Decimal('81'), mercado_destino=MercadoDestino.INTERNO)
            with pytest.raises(ValueError, match='nao pertence'):
                await lote_service.cadastrar_lote(unidade_processamento_id=unidade_b.id, produto_processado_id=produto.id, data_producao=date(2026, 3, 4), quantidade_kg=Decimal('500'), destino_mercado=MercadoDestino.INTERNO)
    asyncio.run(scenario())