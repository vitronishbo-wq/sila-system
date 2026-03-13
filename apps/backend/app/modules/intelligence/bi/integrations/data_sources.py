from __future__ import annotations
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.domain.bridges.intelligence_bi_sources_bridge import DespesaModel, InvoiceModel, OrcamentoModel, PaymentModel, ReceitaModel, StatisticsDataSources

class FinancasDataSource:
    """Metricas financeiras do modulo de pagamentos do cidadao."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        start, next_month = _month_window(data_ref)
        start_dt = datetime.combine(start, datetime.min.time())
        next_month_dt = datetime.combine(next_month, datetime.min.time())
        total_faturas = int(await _scalar(self.db, select(func.count()).select_from(InvoiceModel)))
        faturas_pendentes = int(await _scalar(self.db, select(func.count()).select_from(InvoiceModel).where(func.lower(InvoiceModel.status).in_(('pending', 'issued', 'overdue')))))
        faturas_pagas = int(await _scalar(self.db, select(func.count()).select_from(InvoiceModel).where(func.lower(InvoiceModel.status) == 'paid')))
        valor_faturado_total = _as_float(await _scalar(self.db, select(func.coalesce(func.sum(InvoiceModel.amount), 0))))
        pagamentos_confirmados_mes = int(await _scalar(self.db, select(func.count()).select_from(PaymentModel).where(PaymentModel.created_at >= start_dt, PaymentModel.created_at < next_month_dt, func.lower(PaymentModel.status).in_(('completed', 'reconciled')))))
        valor_pago_mes = _as_float(await _scalar(self.db, select(func.coalesce(func.sum(PaymentModel.amount), 0)).where(PaymentModel.created_at >= start_dt, PaymentModel.created_at < next_month_dt, func.lower(PaymentModel.status).in_(('completed', 'reconciled')))))
        return {'faturas_total': total_faturas, 'faturas_pendentes': faturas_pendentes, 'faturas_pagas': faturas_pagas, 'valor_faturado_total': round(valor_faturado_total, 2), 'pagamentos_confirmados_mes': pagamentos_confirmados_mes, 'valor_pago_mes': round(valor_pago_mes, 2)}

class FinancasPublicasDataSource:
    """Metricas orcamentais consolidadas do modulo de financas publicas."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        _ = data_ref
        orcamentos_total = int(await _scalar(self.db, select(func.count()).select_from(OrcamentoModel)))
        orcamentos_ativos = int(await _scalar(self.db, select(func.count()).select_from(OrcamentoModel).where(func.lower(OrcamentoModel.status).in_(('active', 'ativo', 'vigente', 'em_execucao', 'aprovado')))))
        receitas_previstas = _as_float(await _scalar(self.db, select(func.coalesce(func.sum(ReceitaModel.valor_previsto), 0))))
        receitas_arrecadadas = _as_float(await _scalar(self.db, select(func.coalesce(func.sum(ReceitaModel.valor_arrecadado), 0))))
        despesas_previstas = _as_float(await _scalar(self.db, select(func.coalesce(func.sum(DespesaModel.valor_previsto), 0))))
        despesas_pagas = _as_float(await _scalar(self.db, select(func.coalesce(func.sum(DespesaModel.valor_pago), 0))))
        execucao_despesa = despesas_pagas / despesas_previstas * 100 if despesas_previstas > 0 else 0.0
        cobertura_receita = receitas_arrecadadas / receitas_previstas * 100 if receitas_previstas > 0 else 0.0
        return {'orcamentos_total': orcamentos_total, 'orcamentos_ativos': orcamentos_ativos, 'receitas_previstas_total': round(receitas_previstas, 2), 'receitas_arrecadadas_total': round(receitas_arrecadadas, 2), 'despesas_previstas_total': round(despesas_previstas, 2), 'despesas_pagas_total': round(despesas_pagas, 2), 'execucao_despesa_percentual': round(execucao_despesa, 2), 'cobertura_receita_percentual': round(cobertura_receita, 2)}

class DataSources:
    """Faixada BI para leitura de metricas cross-modulo sem duplicar queries."""
    DOMAIN_ALIASES = {'service-requests': 'service_requests', 'service_requests': 'service_requests', 'assistencia_social': 'assistencia', 'financas-publicas': 'financas_publicas'}

    def __init__(self, clients: dict[str, Any] | None=None):
        self.clients = clients or {}

    @classmethod
    def from_session(cls, db: AsyncSession) -> 'DataSources':
        stats_sources = StatisticsDataSources.from_session(db).as_dict()
        clients: dict[str, Any] = dict(stats_sources)
        clients['financas'] = FinancasDataSource(db)
        clients['financas_publicas'] = FinancasPublicasDataSource(db)
        return cls(clients=clients)

    @classmethod
    def normalize_domain(cls, domain: str) -> str:
        canonical = domain.strip().lower().replace('-', '_')
        return cls.DOMAIN_ALIASES.get(canonical, canonical)

    def as_dict(self) -> dict[str, Any]:
        return dict(self.clients)

    def has_domain(self, domain: str) -> bool:
        canonical = self.normalize_domain(domain)
        return self.clients.get(canonical) is not None

    def available_domains(self) -> list[str]:
        return sorted((name for name, source in self.clients.items() if source is not None))

    async def collect_domain_metrics(self, domain: str, data_ref: date) -> dict[str, float | int]:
        canonical = self.normalize_domain(domain)
        source = self.clients.get(canonical)
        if source is None:
            raise KeyError(canonical)
        return await source.collect_metrics(data_ref)

async def _scalar(db: AsyncSession, statement, default: Any=0) -> Any:
    result = await db.execute(statement)
    value = result.scalar()
    return default if value is None else value

def _month_window(data_ref: date) -> tuple[date, date]:
    start = data_ref.replace(day=1)
    next_month = (start + timedelta(days=32)).replace(day=1)
    return (start, next_month)

def _as_float(value: Decimal | float | int | None) -> float:
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)