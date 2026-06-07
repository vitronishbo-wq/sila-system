from fastapi import APIRouter

from apps.backend.app.platform.integration.metrics_collector import MetricsCollector
from apps.backend.app.platform.integration.provider_registry import ProviderRegistry
from apps.backend.app.platform.integration.models import ProviderStatus
from apps.backend.app.platform.integration.reconciliation.reconciliation_engine import (
    ReconciliationEngine,
)
from apps.backend.app.platform.provider.certification.service import CertificationService
from apps.backend.app.platform.provider.contracts.service import ContractService
from apps.backend.app.platform.provider.sla.snapshot_service import SLASnapshotService
from apps.backend.app.platform.provider.homologation.service import HomologationEvidenceService

router = APIRouter(prefix="/api/providers", tags=["Provider Dashboard"])
_reconciliation = ReconciliationEngine()
_cert_service = CertificationService()
_contract_service = ContractService()
_sla_snap_service = SLASnapshotService()
_homologation_evidence_service = HomologationEvidenceService()


@router.get("")
def list_providers():
    return {
        "providers": [
            {
                "provider": name,
                "status": h.status.value,
                "capability": h.capability.value,
                "version": h.version,
                "enabled": h.enabled,
                "environment": h.environment,
                "owner": h.owner,
                "mock_reason": h.mock_reason,
            }
            for name, h in ProviderRegistry.list_registered().items()
        ]
    }


@router.get("/health")
def provider_health():
    return {
        "summary": ProviderRegistry.get_status_summary(),
        "providers": ProviderRegistry.get_health_summary(),
    }


@router.get("/metrics")
def provider_metrics():
    return MetricsCollector.report()


@router.get("/reconciliation")
def provider_reconciliation():
    reports = _reconciliation.get_all_reports()
    return {
        "reports": {p: r.to_dict() for p, r in reports.items()},
    }


@router.get("/operations")
async def provider_operations():
    providers = list(ProviderRegistry.list_registered().keys())
    rows = []
    for provider in providers:
        cert = await _cert_service.to_dict(provider)
        contract = await _contract_service.to_dict(provider)
        sla = await _sla_snap_service.latest(provider)
        report = _reconciliation.get_last_report(provider)
        health = ProviderRegistry.get(provider)
        rows.append({
            "provider": provider,
            "status": health.status.value if health else "unknown",
            "capability": health.capability.value if health else "unknown",
            "environment": health.environment if health else "dev",
            "owner": health.owner if health else "",
            "enabled": health.enabled if health else False,
            "contract": contract,
            "certification": cert,
            "sla": _sla_snap_service.to_dict(sla) if sla else None,
            "last_reconciliation": report.to_dict() if report else None,
        })
    return {"providers": rows}


_PROMOTION_ORDER = {
    ProviderStatus.MOCK: ProviderStatus.MOCK_LIVE,
    ProviderStatus.MOCK_LIVE: ProviderStatus.HOMOLOGATION,
}


@router.post("/promote/{provider_name}")
async def promote_provider(provider_name: str):
    """Avança um provider na cadeia: MOCK -> MOCK_LIVE -> HOMOLOGATION.
    Nao permite promocao para production."""
    health = ProviderRegistry.get(provider_name)
    if not health:
        return {"ok": False, "error": "provider_nao_encontrado"}

    next_status = _PROMOTION_ORDER.get(health.status)
    if not next_status:
        return {"ok": False, "error": f"{health.status.value} nao pode ser promovido (max HOMOLOGATION)"}

    ProviderRegistry.register(
        provider_name,
        health.capability,
        status=next_status,
        version=health.version,
        sla_target=health.sla_target,
        enabled=health.enabled,
        mock_reason="Promovido para " + next_status.value if next_status != ProviderStatus.REAL else None,
        environment=health.environment,
        owner=health.owner,
    )
    return {"ok": True, "provider": provider_name, "from": health.status.value, "to": next_status.value}


@router.get("/homologation/evidence")
async def homologation_evidence(provider: str | None = None):
    """Evidências auditáveis de homologação institucional."""
    if provider:
        rows = await _homologation_evidence_service.list_by_provider(provider)
    else:
        rows = await _homologation_evidence_service.list_all()
    return {
        "evidence": [_homologation_evidence_service.to_dict(r) for r in rows],
        "summary": await _homologation_evidence_service.summary(),
    }


@router.post("/homologation/evidence")
async def record_homologation_evidence(
    provider: str,
    endpoint: str,
    latency_ms: float | None = None,
    status_code: int | None = None,
    auth_ok: bool = False,
    result: str = "pending",
    operator: str | None = None,
    details: str | None = None,
):
    """Regista uma evidência de homologação manualmente."""
    ev = await _homologation_evidence_service.record(
        provider=provider,
        endpoint=endpoint,
        latency_ms=latency_ms,
        status_code=status_code,
        auth_ok=auth_ok,
        result=result,
        operator=operator,
        details=details,
    )
    return {"ok": True, "evidence": _homologation_evidence_service.to_dict(ev)}
