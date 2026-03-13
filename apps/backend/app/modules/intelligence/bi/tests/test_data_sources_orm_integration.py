from __future__ import annotations
from datetime import date
import pytest
from sqlalchemy import text
from app.modules.intelligence.bi.integrations.data_sources import DataSources
REQUIRED_TABLES_BY_DOMAIN = {'financas': {'financas_invoices', 'financas_payments'}, 'financas_publicas': {'financas_publicas_orcamentos', 'financas_publicas_receitas', 'financas_publicas_despesas'}}

async def _domain_has_all_tables(db_session, tables: set[str]) -> bool:
    for table_name in tables:
        result = await db_session.execute(text('SELECT to_regclass(:table_name)'), {'table_name': f'public.{table_name}'})
        if result.scalar() is None:
            return False
    return True

@pytest.mark.asyncio
@pytest.mark.integration
async def test_data_sources_collect_metrics_with_real_orm(db_session) -> None:
    sources = DataSources.from_session(db_session)
    eligible_domains: list[str] = []
    tested_domains: list[str] = []
    for domain, required_tables in REQUIRED_TABLES_BY_DOMAIN.items():
        if not await _domain_has_all_tables(db_session, required_tables):
            continue
        eligible_domains.append(domain)
        if not sources.has_domain(domain):
            continue
        metrics = await sources.collect_domain_metrics(domain, date.today())
        assert isinstance(metrics, dict)
        assert metrics
        assert all((isinstance(value, (int, float)) for value in metrics.values()))
        tested_domains.append(domain)
    if not eligible_domains:
        assert sources.has_domain('financas')
        assert sources.has_domain('financas_publicas')
        return
    assert tested_domains, 'Dominios com tabela fisica existem, mas nenhum adapter BI conseguiu coletar metricas.'