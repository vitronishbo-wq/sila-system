from __future__ import annotations
from datetime import date, datetime
from typing import Any
from app.modules.intelligence.bi.integrations.data_sources import DataSources

class DashboardService:
    """Servico de dashboards com agregacao multi-dominio resiliente."""

    def __init__(self, data_sources: DataSources):
        self.data_sources = data_sources

    def has_domain_source(self, domain: str) -> bool:
        return self.data_sources.has_domain(domain)

    def available_domains(self) -> list[str]:
        return self.data_sources.available_domains()

    async def get_dashboard_domain(self, domain: str, data_ref: date | None=None) -> dict[str, Any]:
        ref = data_ref or date.today()
        canonical = self.data_sources.normalize_domain(domain)
        metrics = await self.data_sources.collect_domain_metrics(canonical, ref)
        return {'domain': canonical, 'reference_date': ref.isoformat(), 'generated_at': datetime.utcnow().isoformat(), 'metrics': metrics, 'metric_count': len(metrics)}

    async def get_dashboard_executivo(self, data_ref: date | None=None, domains: list[str] | None=None) -> dict[str, Any]:
        ref = data_ref or date.today()
        selected_domains = domains or self.available_domains()
        data_by_domain: dict[str, dict[str, float | int]] = {}
        unavailable_domains: list[str] = []
        errors: dict[str, str] = {}
        for raw_domain in selected_domains:
            domain = self.data_sources.normalize_domain(raw_domain)
            if not self.has_domain_source(domain):
                unavailable_domains.append(domain)
                continue
            try:
                data_by_domain[domain] = await self.data_sources.collect_domain_metrics(domain, ref)
            except Exception as exc:
                errors[domain] = str(exc)
        summary = self._build_executive_summary(data_by_domain, unavailable_domains, errors)
        return {'reference_date': ref.isoformat(), 'generated_at': datetime.utcnow().isoformat(), 'summary': summary, 'domains': data_by_domain, 'unavailable_domains': sorted(set(unavailable_domains)), 'errors': errors}

    @staticmethod
    def _build_executive_summary(data_by_domain: dict[str, dict[str, float | int]], unavailable_domains: list[str], errors: dict[str, str]) -> dict[str, Any]:
        return {'domains_requested': len(data_by_domain) + len(unavailable_domains) + len(errors), 'domains_with_data': len(data_by_domain), 'domains_unavailable': len(set(unavailable_domains)), 'domains_with_error': len(errors), 'total_indicadores': sum((len(metrics) for metrics in data_by_domain.values())), 'indicadores_chave': {'cidadaos_ativos': _sum_metric_fragment(data_by_domain, 'cidadaos_ativos'), 'atendimentos_mes': _sum_metric_fragment(data_by_domain, 'atendimentos_mes'), 'requests_total_mes': _sum_metric_fragment(data_by_domain, 'requests_total_mes'), 'valor_pago_mes': _sum_metric_fragment(data_by_domain, 'valor_pago_mes'), 'despesas_pagas_total': _sum_metric_fragment(data_by_domain, 'despesas_pagas_total')}}

def _sum_metric_fragment(data_by_domain: dict[str, dict[str, float | int]], fragment: str) -> float:
    total = 0.0
    for metrics in data_by_domain.values():
        for key, value in metrics.items():
            if fragment in key and isinstance(value, (int, float)):
                total += float(value)
    return round(total, 2)