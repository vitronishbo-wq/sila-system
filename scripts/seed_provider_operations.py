import asyncio
import logging
import random
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "/home/dev03wsl/sila-system")
sys.path.insert(0, "/home/dev03wsl/sila-system/apps/backend")

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("seed_provider_operations")

from apps.backend.app.platform.integration.provider_registry import (
    ProviderRegistry,
    register_default_providers,
)

# Reuse module-level engine so /api/providers/reconciliation sees seeded data
from apps.backend.app.platform.integration import provider_router as _provider_router

from apps.backend.app.platform.integration.reconciliation.reconciliation_report import (
    ReconciliationReport,
    ReconciliationStatus,
)
from apps.backend.app.platform.provider.certification.service import (
    CertificationService,
    CertificationStatus,
)
from apps.backend.app.platform.provider.contracts.service import (
    ContractService,
    ContractStatus,
)
from apps.backend.app.platform.provider.sla.snapshot_service import SLASnapshotService

PROVIDER_NAMES = [
    "multicaixa", "agt", "xroad_bi", "registo_civil",
    "emis", "tcu", "financas_publicas", "anatel",
]


async def seed():
    register_default_providers()
    cert_svc = CertificationService()
    contract_svc = ContractService()
    sla_svc = SLASnapshotService()

    logger.info("=" * 60)
    logger.info("Seeding Provider Operations Test Data")
    logger.info("=" * 60)

    # ── PASSO 2: Contratos de Teste ──────────────────────────────
    logger.info("\n--- PASSO 2: Contratos de Teste ---")
    for provider in PROVIDER_NAMES:
        num = provider.upper()[:5] + "-TC-001"
        await contract_svc.register(
            provider=provider,
            contract_number=num,
            entity="sila_qa",
            status=ContractStatus.TESTING,
        )

    # ── PASSO 3: Certificacoes (testing) ────────────────────────
    logger.info("\n--- PASSO 3: Certificacoes (testing) ---")
    for provider in PROVIDER_NAMES:
        await cert_svc.set_status(
            provider=provider,
            status=CertificationStatus.TESTING,
            environment="homologacao",
            notes="Certificacao de teste para homologacao interna",
        )

    # ── PASSO 4: SLA Simulado ───────────────────────────────────
    logger.info("\n--- PASSO 4: SLA Simulado ---")
    for provider in PROVIDER_NAMES:
        # Feed synthetic latencies so snapshot has data
        sla_engine = sla_svc._sla_engine
        for _ in range(200):
            sla_engine.record_request(provider, random.uniform(50, 800), success=True)
        sla_engine.record_request(provider, random.uniform(900, 2000), success=False)
        snap = await sla_svc.take_snapshot(provider, measurement_mode="simulated")
        logger.info(f"  SLA Snapshot: {provider} -> avail={snap.availability:.1f}% p95={snap.latency_p95:.0f}ms")

    # ── PASSO 5: Reconciliacao de Teste ─────────────────────────
    logger.info("\n--- PASSO 5: Reconciliacao de Teste ---")
    for provider in PROVIDER_NAMES:
        missing_internal = {f"TX{n:06d}" for n in range(1, 31)}
        missing_provider = {f"TX{n:06d}" for n in range(500, 521)}
        amount_mismatches = [
            {"ref": f"TX{n:06d}", "internal": 1500.0 + n, "provider": 1450.0 + n, "diff": 50.0}
            for n in range(100, 115)
        ]
        divergences = [*missing_internal, *missing_provider, *amount_mismatches]

        report = ReconciliationReport(
            provider=provider,
            status=ReconciliationStatus.DIVERGENCE_FOUND,
            internal_count=1000,
            provider_count=1000,
            matched_count=1000 - len(divergences),
            divergences=divergences[:10],
            total_amount_internal=1500000.0,
            total_amount_provider=1495000.0,
            scenario="test",
        )
        _provider_router._reconciliation._history[provider] = report
        logger.info(f"  Reconciliation: {provider} -> divergence_found, divergences={len(divergences)}")

    logger.info("\n" + "=" * 60)
    logger.info("Seed complete. System is READY_FOR_HOMOLOGATION.")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(seed())

    # Verify inline — same process, same in-memory state
    from fastapi.testclient import TestClient
    from apps.backend.app.platform.integration.provider_router import router
    from apps.backend.app.platform.runtime.health_router import router as health_router
    from fastapi import FastAPI
    _app = FastAPI()
    _app.include_router(health_router)
    _app.include_router(router)
    _client = TestClient(_app)

    r = _client.get("/api/providers")
    d = r.json()
    logger.info(f"  Providers registered: {len(d['providers'])}")
    for p in d["providers"]:
        logger.info(f"    {p['provider']:20s} status={p['status']:12s}")

    r = _client.get("/api/providers/reconciliation")
    d = r.json()
    logger.info(f"  Reconciliation reports: {len(d.get('reports', {}))}")
    for pn, rep in d.get("reports", {}).items():
        logger.info(f"    {pn:20s} status={rep['status']:18s} divergences={rep['divergences']} scenario={rep.get('scenario','')}")

    r2 = _client.get("/api/providers/operations")
    o = r2.json()
    for pd in o["providers"]:
        rec = pd.get("last_reconciliation")
        sla = pd.get("sla")
        logger.info(
            f"    {pd['provider']:20s} "
            f"contract={pd['contract']['status']} "
            f"cert={pd['certification']['status']} "
            f"sla_avail={sla['availability']:.1f}% meas={sla.get('measurement_mode','')} "
            f"recon={rec['status'] if rec else '-:-'}"
        )

    logger.info("\nAll endpoints verified. READY_FOR_HOMOLOGATION.")
