from __future__ import annotations
import os
from decimal import Decimal
from uuid import uuid4
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import TipoAlvara, TipoHabiteSe, TipoLoteamento, TipoOperacaoUrbana, TipoParcelamento, TipoPlanoDiretor, TipoZona, UsoPermitido
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.alvara import Alvara
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.habite_se import HabiteSe
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.licenca_urbanistica import LicencaUrbanistica
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.loteamento import Loteamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.operacao_urbana import OperacaoUrbana
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.parcelamento import Parcelamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.plano_diretor import PlanoDiretor
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.zoneamento import Zoneamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import SQLAlchemyAlvaraRepository, SQLAlchemyHabiteSeRepository, SQLAlchemyLicencaUrbanisticaRepository, SQLAlchemyLoteamentoRepository, SQLAlchemyOperacaoUrbanaRepository, SQLAlchemyParcelamentoRepository, SQLAlchemyPlanoDiretorRepository, SQLAlchemyZoneamentoRepository
TABLES = ['urbanismo_habitacao_planos_diretores', 'urbanismo_habitacao_zoneamentos', 'urbanismo_habitacao_operacoes_urbanas', 'urbanismo_habitacao_parcelamentos', 'urbanismo_habitacao_loteamentos', 'urbanismo_habitacao_licencas_urbanisticas', 'urbanismo_habitacao_alvaras', 'urbanismo_habitacao_habite_se']

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
    assert result.scalar_one_or_none() is not None, f'Tabela fisica ausente: {table_name}. Execute migration 20260304_036_urbanismo_habitacao_orm_core.'

@pytest.mark.asyncio
@pytest.mark.integration
async def test_repositories_urbanismo_habitacao_roundtrip_orm_real(db_session: AsyncSession) -> None:
    for table_name in TABLES:
        await _assert_table_exists(db_session, table_name)
    plano_repo = SQLAlchemyPlanoDiretorRepository(db_session)
    zone_repo = SQLAlchemyZoneamentoRepository(db_session)
    operacao_repo = SQLAlchemyOperacaoUrbanaRepository(db_session)
    parcelamento_repo = SQLAlchemyParcelamentoRepository(db_session)
    loteamento_repo = SQLAlchemyLoteamentoRepository(db_session)
    licenca_repo = SQLAlchemyLicencaUrbanisticaRepository(db_session)
    alvara_repo = SQLAlchemyAlvaraRepository(db_session)
    habite_repo = SQLAlchemyHabiteSeRepository(db_session)
    plano = await plano_repo.save(PlanoDiretor.criar(codigo_plano=await plano_repo.next_codigo(), nome='Plano Diretor ORM Real', tipo=TipoPlanoDiretor.MUNICIPAL, provincia='Luanda', ano_elaboracao=2026, orgao_responsavel_id=uuid4()))
    zoneamento = await zone_repo.save(Zoneamento.criar(codigo_zoneamento=await zone_repo.next_codigo(), nome='Zona Residencial ORM', tipo_zona=TipoZona.RESIDENCIAL, plano_diretor_id=plano.id, provincia='Luanda', usos_permitidos=[UsoPermitido.HABITACIONAL, UsoPermitido.SERVICOS]))
    operacao = await operacao_repo.save(OperacaoUrbana.criar(codigo_operacao=await operacao_repo.next_codigo(), nome='Operacao Urbana ORM', tipo=TipoOperacaoUrbana.OPERACAO_URBANA_CONSORCIADA, plano_diretor_id=plano.id, orgao_responsavel_id=uuid4(), provincia='Luanda', investimento_previsto=Decimal('2500000.00')))
    parcelamento = await parcelamento_repo.save(Parcelamento.criar(codigo_parcelamento=await parcelamento_repo.next_codigo(), nome='Parcelamento ORM', tipo=TipoParcelamento.LOTEAMENTO, plano_diretor_id=plano.id, zoneamento_id=zoneamento.id, provincia='Luanda', area_total=Decimal('55000.00'), quantidade_unidades_prevista=180))
    loteamento = await loteamento_repo.save(Loteamento.criar(codigo_loteamento=await loteamento_repo.next_codigo(), nome='Loteamento ORM', tipo=TipoLoteamento.ABERTO, parcelamento_id=parcelamento.id, plano_diretor_id=plano.id, zoneamento_id=zoneamento.id, provincia='Luanda', area_total=Decimal('42000.00'), quantidade_lotes_prevista=120))
    licenca = await licenca_repo.save(LicencaUrbanistica.criar(codigo_licenca=await licenca_repo.next_codigo(), numero_processo='PROC-URB-ORM-001', tipo_alvara=TipoAlvara.CONSTRUCAO, requerente_id=uuid4(), zoneamento_id=zoneamento.id, provincia='Luanda'))
    alvara = await alvara_repo.save(Alvara.criar(codigo_alvara=await alvara_repo.next_codigo(), numero_processo='PROC-ALV-ORM-001', tipo=TipoAlvara.CONSTRUCAO, licenca_urbanistica_id=licenca.id, requerente_id=uuid4(), provincia='Luanda'))
    habite = await habite_repo.save(HabiteSe.criar(codigo_habite_se=await habite_repo.next_codigo(), numero_processo='PROC-HBT-ORM-001', tipo=TipoHabiteSe.TOTAL, alvara_id=alvara.id, requerente_id=uuid4(), provincia='Luanda'))
    assert await plano_repo.get_by_codigo(plano.codigo_plano) is not None
    assert await zone_repo.get_by_codigo(zoneamento.codigo_zoneamento) is not None
    assert await operacao_repo.get_by_codigo(operacao.codigo_operacao) is not None
    assert await parcelamento_repo.get_by_codigo(parcelamento.codigo_parcelamento) is not None
    assert await loteamento_repo.get_by_codigo(loteamento.codigo_loteamento) is not None
    assert await licenca_repo.get_by_codigo(licenca.codigo_licenca) is not None
    assert await alvara_repo.get_by_codigo(alvara.codigo_alvara) is not None
    assert await habite_repo.get_by_codigo(habite.codigo_habite_se) is not None
    assert len(await plano_repo.list(provincia='luanda')) >= 1
    assert len(await zone_repo.list(provincia='LUANDA')) >= 1
    assert len(await operacao_repo.list(provincia='Luanda')) >= 1
    assert len(await parcelamento_repo.list(provincia='Luanda')) >= 1
    assert len(await loteamento_repo.list(provincia='Luanda')) >= 1
    assert len(await licenca_repo.list(provincia='Luanda')) >= 1
    assert len(await alvara_repo.list(provincia='Luanda')) >= 1
    assert len(await habite_repo.list(provincia='Luanda')) >= 1