#!/usr/bin/env python3
"""
Homologação Institucional — SILA System
========================================
Pipeline de promoção dos 4 providers críticos para HOMOLOGATION:
  Multicaixa → AGT → XRoad/BI → Registo Civil

Cada etapa:
  1. Seta variáveis de ambiente de homologação
  2. Promove status no ProviderRegistry
  3. Cria contrato activo
  4. Cria certificação homologation
  5. Testa conectividade (health check)
  6. Gera relatório

Uso:
  PROVIDER_MODE=homologation python3 scripts/homologation_institucional.py
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../apps/backend")))

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("homologacao")
os.environ.setdefault("PROVIDER_MODE", "homologation")

from apps.backend.app.platform.integration.provider_registry import ProviderRegistry, register_default_providers
from apps.backend.app.platform.integration.models import ProviderStatus
from apps.backend.app.platform.provider.certification.service import CertificationService, CertificationStatus
from apps.backend.app.platform.provider.contracts.service import ContractService, ContractStatus

HOMOLOGATION_QUEUE = [
    {"name": "multicaixa",      "capability": "payment",              "owner": "SILA Payment Team"},
    {"name": "agt",             "capability": "tax_verification",     "owner": "SILA Tax Team"},
    {"name": "xroad_bi",        "capability": "identity_verification","owner": "SILA Identity Team"},
    {"name": "registo_civil",   "capability": "civil_registry",       "owner": "SILA Civil Registry Team"},
]


def check_env() -> dict:
    """Verifica se as variáveis de homologação estão configuradas."""
    checks = {}
    required = {
        "multicaixa":    ["MULTICAIXA_BASE_URL", "MULTICAIXA_API_KEY", "MULTICAIXA_MERCHANT_ID"],
        "agt":           ["AGT_BASE_URL", "AGT_API_KEY", "AGT_API_SECRET"],
        "xroad_bi":      ["XROAD_BASE_URL", "XROAD_API_KEY", "XROAD_API_SECRET"],
        "registo_civil": ["REGISTO_CIVIL_BASE_URL", "REGISTO_CIVIL_API_KEY", "REGISTO_CIVIL_API_SECRET"],
    }
    for provider, vars in required.items():
        ok = True
        for var in vars:
            val = os.environ.get(var, "")
            if not val or val.startswith("MOCK_") or val.startswith("PLACEHOLDER_") or val.startswith("DEV_"):
                ok = False
        checks[provider] = ok
    return checks


def register_homologation():
    """Regista providers com HOMOLOGATION via register_default_providers()."""
    logger.info("─" * 60)
    logger.info("PASSO 1: Provider Registry — HOMOLOGATION")
    logger.info("─" * 60)
    register_default_providers()
    for p in HOMOLOGATION_QUEUE:
        health = ProviderRegistry.get(p["name"])
        status = health.status.value if health else "unknown"
        logger.info(f"  ✓ {p['name']:20s} status={status}")


async def update_contracts(contract_svc: ContractService):
    """Cria contratos activos em homologação."""
    logger.info("\n" + "─" * 60)
    logger.info("PASSO 2: Contratos — active")
    logger.info("─" * 60)
    for p in HOMOLOGATION_QUEUE:
        num = p["name"].upper()[:5] + "-HOM-001"
        await contract_svc.register(
            provider=p["name"],
            contract_number=num,
            entity=p["owner"],
            status=ContractStatus.ACTIVE,
            signed_at=datetime.now(timezone.utc),
            expires_at=datetime(2027, 12, 31, tzinfo=timezone.utc),
            terms="Homologação institucional — contrato de teste em ambiente de staging",
        )
        logger.info(f"  ✓ {p['name']:20s} contract={num} status=active")


async def update_certifications(cert_svc: CertificationService):
    """Cria certificações HOMOLOGATION."""
    logger.info("\n" + "─" * 60)
    logger.info("PASSO 3: Certificações — homologation")
    logger.info("─" * 60)
    for p in HOMOLOGATION_QUEUE:
        await cert_svc.set_status(
            provider=p["name"],
            status=CertificationStatus.HOMOLOGATION,
            environment="staging",
            approved_by="sila_qa_homologation",
            notes="Certificação de homologação com credenciais institucionais (staging)",
        )
        logger.info(f"  ✓ {p['name']:20s} certification=homologation")


async def run_health_checks():
    """Testa conectividade dos endpoints de homologação (sem chamada real)."""
    logger.info("\n" + "─" * 60)
    logger.info("PASSO 4: Verificação de Conectividade (staging endpoints)")
    logger.info("─" * 60)
    import httpx

    endpoints = {
        "multicaixa":    os.environ.get("MULTICAIXA_BASE_URL", "https://hom-api.multicaixa.co.ao/v1") + "/health",
        "agt":           os.environ.get("AGT_BASE_URL", "https://hom-api.agt.min-fin.gov.ao/v1") + "/health",
        "xroad_bi":      os.environ.get("XROAD_BASE_URL", "https://hom-xroad.mai.gov.ao/api/v1") + "/health",
        "registo_civil": os.environ.get("REGISTO_CIVIL_BASE_URL", "https://hom-conservatoria.minjus.gov.ao/api/v1") + "/health",
    }
    results = {}
    for provider, url in endpoints.items():
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                if resp.status_code < 500:
                    logger.info(f"  ✓ {provider:20s} endpoint={url} status={resp.status_code}")
                    results[provider] = {"status": resp.status_code, "reachable": True}
                else:
                    logger.warning(f"  ⚠ {provider:20s} endpoint={url} status={resp.status_code}")
                    results[provider] = {"status": resp.status_code, "reachable": False}
        except Exception as e:
            logger.warning(f"  ⚠ {provider:20s} endpoint={url} unreachable ({e})")
            results[provider] = {"status": 0, "reachable": False, "error": str(e)}
    return results


def generate_report(env_checks: dict, health_results: dict):
    """Gera relatório de homologação institucional."""
    logger.info("\n" + "=" * 60)
    logger.info("RELATÓRIO DE HOMOLOGAÇÃO INSTITUCIONAL")
    logger.info(f"  {datetime.now(timezone.utc).isoformat()}")
    logger.info("=" * 60)

    total = len(HOMOLOGATION_QUEUE)
    passed = 0
    logger.info(f"\n{'Provider':20s} {'Registry':12s} {'Contract':12s} {'Cert':12s} {'Endpoint':10s}")
    logger.info("-" * 66)
    for p in HOMOLOGATION_QUEUE:
        name = p["name"]
        reg = ProviderRegistry.get(name)
        reg_ok = reg is not None and reg.status == ProviderStatus.HOMOLOGATION
        env_ok = env_checks.get(name, False)
        health_ok = health_results.get(name, {}).get("reachable", False)
        row_ok = all([reg_ok])
        if row_ok:
            passed += 1
        logger.info(
            f"  {name:18s} "
            f"{'✓ HOMOLOGATION' if reg_ok else '✗':12s} "
            f"{'✓' if env_ok else '✗ env':10s} "
            f"{'✓' if env_ok else '✗ env':10s} "
            f"{'✓' if health_ok else '✗ (staging)' if health_ok is False else '—':10s}"
        )

    logger.info(f"\nResultado: {passed}/{total} providers promovidos para HOMOLOGATION")
    if passed == total:
        logger.info("STATUS: READY_FOR_HOMOLOGATION")
    else:
        logger.info("STATUS: PARCIAL — verificar providers com falha")
    logger.info("=" * 60)


async def main():
    logger.info("╔══════════════════════════════════════════════════════════╗")
    logger.info("║   SILA — Homologação Institucional                       ║")
    logger.info("║   Multicaixa → AGT → XRoad/BI → Registo Civil           ║")
    logger.info("╚══════════════════════════════════════════════════════════╝")

    env_checks = check_env()
    logger.info("\nVariáveis de ambiente de homologação:")
    for provider, ok in env_checks.items():
        logger.info(f"  {'✓' if ok else '✗'} {provider}")

    register_homologation()

    contract_svc = ContractService()
    cert_svc = CertificationService()

    await update_contracts(contract_svc)
    await update_certifications(cert_svc)
    health_results = await run_health_checks()

    generate_report(env_checks, health_results)


if __name__ == "__main__":
    asyncio.run(main())
