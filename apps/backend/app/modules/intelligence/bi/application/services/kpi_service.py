from __future__ import annotations
from datetime import date, datetime
from typing import Any
from app.modules.intelligence.bi.integrations.data_sources import DataSources

class KPIService:
    """Faixada de KPIs para o modulo BI."""

    def __init__(self, data_sources: DataSources):
        self.data_sources = data_sources

    def has_domain_source(self, domain: str) -> bool:
        return self.data_sources.has_domain(domain)

    def available_domains(self) -> list[str]:
        return self.data_sources.available_domains()

    async def get_domain_kpis(self, domain: str, data_ref: date | None=None) -> dict[str, Any]:
        ref = data_ref or date.today()
        canonical = self.data_sources.normalize_domain(domain)
        metrics = await self.data_sources.collect_domain_metrics(canonical, ref)
        return {'domain': canonical, 'reference_date': ref.isoformat(), 'generated_at': datetime.utcnow().isoformat(), 'metrics': metrics, 'metric_count': len(metrics)}

    async def get_consolidated_kpis(self, data_ref: date | None=None, domains: list[str] | None=None) -> dict[str, Any]:
        ref = data_ref or date.today()
        requested_domains = domains or self.available_domains()
        consolidated: dict[str, dict[str, float | int]] = {}
        unavailable: list[str] = []
        errors: dict[str, str] = {}
        for raw_domain in requested_domains:
            domain = self.data_sources.normalize_domain(raw_domain)
            if not self.has_domain_source(domain):
                unavailable.append(domain)
                continue
            try:
                consolidated[domain] = await self.data_sources.collect_domain_metrics(domain, ref)
            except Exception as exc:
                errors[domain] = str(exc)
        return {'reference_date': ref.isoformat(), 'generated_at': datetime.utcnow().isoformat(), 'domains': consolidated, 'unavailable_domains': sorted(set(unavailable)), 'errors': errors}