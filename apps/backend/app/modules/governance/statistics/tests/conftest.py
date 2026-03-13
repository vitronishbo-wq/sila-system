from __future__ import annotations
from collections.abc import AsyncGenerator, Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.api.deps import get_db
from apps.backend.app.modules.governance.statistics.api.router import router as estatistica_router
from apps.backend.app.modules.governance.statistics.infrastructure.models.agregacao_model import AgregacaoModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.alerta_model import AlertaModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.analise_model import AnaliseModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.comparativo_model import ComparativoModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.dashboard_model import DashboardModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.exportacao_model import ExportacaoModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.indicador_model import IndicadorModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.kpi_model import KPIModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.metrica_model import MetricaModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.outbox_event_model import OutboxEventModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.previsao_model import PrevisaoModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.ranking_model import RankingModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.relatorio_model import RelatorioModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.tendencia_model import TendenciaModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.timeseries_model import TimeSeriesModel
TABLES = [MetricaModel.__table__, KPIModel.__table__, TimeSeriesModel.__table__, DashboardModel.__table__, RelatorioModel.__table__, IndicadorModel.__table__, AgregacaoModel.__table__, ExportacaoModel.__table__, AnaliseModel.__table__, PrevisaoModel.__table__, ComparativoModel.__table__, RankingModel.__table__, TendenciaModel.__table__, AlertaModel.__table__, OutboxEventModel.__table__]

@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def setup() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: MetricaModel.metadata.create_all(sync_conn, tables=TABLES))

    async def teardown() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: MetricaModel.metadata.drop_all(sync_conn, tables=TABLES))
        await engine.dispose()
    import asyncio
    asyncio.run(setup())

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session
    app = FastAPI()
    app.include_router(estatistica_router, prefix='/api/v1')
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    asyncio.run(teardown())