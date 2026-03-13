from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
import os
from uuid import uuid4
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.modules.infrastructure.domain.enums import NaturezaObra, StatusEdital, StatusLicitacao, StatusObra, StatusProjeto, TipoAditivo, TipoLicitacao, TipoObra, TipoProjeto
from app.modules.infrastructure.domain.models.aditivo_contratual import AditivoContratual
from app.modules.infrastructure.domain.models.edital import Edital
from app.modules.infrastructure.domain.models.fiscalizacao_obra import FiscalizacaoObra
from app.modules.infrastructure.domain.models.licitacao import Licitacao
from app.modules.infrastructure.domain.models.medicao_obra import MedicaoObra
from app.modules.infrastructure.domain.models.obra import Obra
from app.modules.infrastructure.domain.models.projeto_obra import ProjetoObra
from app.modules.infrastructure.domain.models.termo_recebimento import TermoRecebimento
from app.modules.infrastructure.infrastructure.repositories import SQLAlchemyEditalRepository, SQLAlchemyLicitacaoRepository, SQLAlchemyObraRepository, SQLAlchemyProjetoRepository
TABLES = ['obras_publicas_projetos', 'obras_publicas_obras', 'obras_publicas_licitacoes', 'obras_publicas_editais']

def _get_database_url() -> str:
    url = os.environ.get('DATABASE_URL', 'postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db')
    if 'sqlite' in url:
        raise RuntimeError('Testes ORM reais exigem PostgreSQL')
    if url.startswith('postgresql://'):
        return url.replace('postgresql://', 'postgresql+asyncpg://', 1)
    return url

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(_get_database_url(), echo=False, poolclass=NullPool)
    async with engine.connect() as conn:
        trans = await conn.begin()
        factory = sessionmaker(bind=conn, class_=AsyncSession, expire_on_commit=False, autocommit=False)
        async with factory() as session:
            await session.begin()
            try:
                yield session
            finally:
                try:
                    await session.rollback()
                except Exception:
                    pass
        try:
            await trans.rollback()
        except Exception:
            pass
    await engine.dispose()

async def _assert_table_exists(db_session: AsyncSession, table_name: str) -> None:
    result = await db_session.execute(text('SELECT to_regclass(:table_name)'), {'table_name': table_name})
    assert result.scalar_one_or_none() is not None, f'Tabela fisica ausente: {table_name}. Execute migration 20260304_037_obras_publicas_orm_core.'

@pytest.mark.asyncio
@pytest.mark.integration
async def test_repositories_obras_publicas_roundtrip_orm_real(db_session: AsyncSession) -> None:
    for table_name in TABLES:
        await _assert_table_exists(db_session, table_name)
    projeto_repo = SQLAlchemyProjetoRepository(db_session)
    obra_repo = SQLAlchemyObraRepository(db_session)
    licitacao_repo = SQLAlchemyLicitacaoRepository(db_session)
    edital_repo = SQLAlchemyEditalRepository(db_session)
    projeto = await projeto_repo.save(ProjetoObra.criar(codigo_projeto=await projeto_repo.next_codigo(), nome='Projeto Integrado Terminal Norte', tipo=TipoProjeto.EXECUTIVO, orgao_responsavel_id=uuid4(), responsavel_tecnico_id=uuid4(), valor_estimado=Decimal('3200000.00'), data_inicio_prevista=date.today(), data_fim_prevista=date.today() + timedelta(days=120)))
    assert projeto.status == StatusProjeto.ELABORACAO
    obra = Obra.criar(codigo_obra=await obra_repo.next_codigo(), nome='Obra Terminal Norte', tipo=TipoObra.CONSTRUCAO, natureza=NaturezaObra.NOVA, orgao_responsavel_id=uuid4(), orgao_responsavel_tipo='ministerio', valor_orcado=Decimal('5000000.00'), data_inicio_prevista=date.today(), data_fim_prevista=date.today() + timedelta(days=300), endereco='Av. Integracao', bairro='Centro', municipio='Luanda', provincia='Luanda')
    obra.projeto_id = projeto.id
    obra.iniciar_licitacao()
    obra.contratar(contrato_id=uuid4(), empreiteira_id=uuid4(), valor=Decimal('4900000.00'))
    obra.iniciar_execucao(date.today())
    obra.registrar_medicao_detalhada(MedicaoObra.registrar(periodo_referencia='2026-03', valor_medido=Decimal('350000.00'), percentual_executado=Decimal('14.00'), fiscal_id=uuid4(), documentos=['medicao-marco.pdf']))
    obra.registrar_aditivo(AditivoContratual.registrar(tipo=TipoAditivo.PRAZO, justificativa='Ajuste de cronograma', prazo_adicional_dias=20))
    obra.registrar_fiscalizacao(FiscalizacaoObra.registrar(fiscal_id=uuid4(), conformidade=True, apontamentos='Sem nao conformidades'))
    obra.concluir(date.today() + timedelta(days=280))
    obra.registrar_termo_recebimento(TermoRecebimento.registrar(tipo='definitivo', responsavel_id=uuid4(), data_termo=date.today() + timedelta(days=285)))
    obra.registrar_evento_auditoria(evento='obra_roundtrip_orm_real')
    obra_salva = await obra_repo.save(obra)
    assert obra_salva.status == StatusObra.ENTREGUE
    licitacao = await licitacao_repo.save(Licitacao.abrir(numero_licitacao=await licitacao_repo.next_numero(), objeto='Contratacao principal da obra', tipo=TipoLicitacao.CONCORRENCIA, obra_id=obra_salva.id, orgao_responsavel_id=obra_salva.orgao_responsavel_id, valor_estimado=Decimal('4900000.00'), data_publicacao_edital=date.today(), data_entrega_propostas=date.today() + timedelta(days=20)))
    assert licitacao.status == StatusLicitacao.EDITAL_PUBLICADO
    edital = await edital_repo.save(Edital.publicar(numero_edital=await edital_repo.next_numero(), titulo='Edital Obra Terminal Norte', objeto='Execucao da obra terminal norte', licitacao_id=licitacao.id, data_publicacao=date.today(), data_abertura=date.today() + timedelta(days=5), data_encerramento=date.today() + timedelta(days=25)))
    assert edital.status == StatusEdital.PUBLICADO
    obra_db = await obra_repo.get_by_codigo(obra_salva.codigo_obra)
    assert obra_db is not None
    assert obra_db.status == StatusObra.ENTREGUE
    assert len(obra_db.medicoes) == 1
    assert len(obra_db.aditivos) == 1
    assert len(obra_db.fiscalizacoes) == 1
    assert len(obra_db.termos_recebimento) == 1
    assert len(obra_db.trilha_auditoria) >= 1
    assert len(await obra_repo.list(status=StatusObra.ENTREGUE, provincia='LUANDA')) >= 1
    assert len(await projeto_repo.list(status=StatusProjeto.ELABORACAO, tipo=TipoProjeto.EXECUTIVO)) >= 1
    assert len(await licitacao_repo.list(status=StatusLicitacao.EDITAL_PUBLICADO, obra_id=obra_salva.id)) >= 1
    assert len(await edital_repo.list(status=StatusEdital.PUBLICADO, licitacao_id=licitacao.id)) >= 1
