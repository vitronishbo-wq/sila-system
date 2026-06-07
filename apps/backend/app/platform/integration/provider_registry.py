import logging
from datetime import datetime, timezone
from typing import Optional

from apps.backend.app.platform.integration.models import (
    ProviderCapability,
    ProviderHealth,
    ProviderMetrics,
    ProviderStatus,
)

logger = logging.getLogger(__name__)


class ProviderRegistry:
    _providers: dict[str, ProviderHealth] = {}

    @classmethod
    def register(
        cls,
        provider: str,
        capability: ProviderCapability,
        status: ProviderStatus = ProviderStatus.MOCK,
        version: str = "0.0.0",
        sla_target: Optional[float] = None,
        enabled: bool = True,
        mock_reason: Optional[str] = None,
        environment: str = "dev",
        owner: str = "",
    ) -> ProviderHealth:
        health = ProviderHealth(
            provider=provider,
            status=status,
            capability=capability,
            version=version,
            sla_target=sla_target,
            enabled=enabled,
            mock_reason=mock_reason,
            environment=environment,
            owner=owner,
        )
        cls._providers[provider] = health
        logger.info(
            "provider_registered name=%s status=%s capability=%s",
            provider, status.value, capability.value,
        )
        return health

    @classmethod
    def get(cls, provider: str) -> Optional[ProviderHealth]:
        return cls._providers.get(provider)

    @classmethod
    def list_registered(cls) -> dict[str, ProviderHealth]:
        return dict(cls._providers)

    @classmethod
    def record_success(cls, provider: str, latency: float) -> None:
        health = cls._providers.get(provider)
        if not health:
            return
        now = datetime.now(timezone.utc)
        health.last_success = now
        health.metrics.last_success = now
        health.metrics.last_latency = latency
        health.metrics.success_count += 1
        health.metrics.last_error_message = None
        _update_latency_percentiles(health.metrics, latency)

    @classmethod
    def record_error(cls, provider: str, latency: float, error_message: str) -> None:
        health = cls._providers.get(provider)
        if not health:
            return
        now = datetime.now(timezone.utc)
        health.metrics.last_error = now
        health.metrics.last_error_message = error_message
        health.metrics.last_latency = latency
        health.metrics.error_count += 1
        _update_latency_percentiles(health.metrics, latency)

    @classmethod
    def clear(cls) -> None:
        cls._providers.clear()

    @classmethod
    def get_status_summary(cls) -> dict[str, str]:
        return {
            name: h.status.value
            for name, h in cls._providers.items()
        }

    @classmethod
    def get_health_summary(cls) -> list[dict]:
        return [h.to_health_dict() for h in cls._providers.values()]


def _update_latency_percentiles(metrics: ProviderMetrics, latency: float) -> None:
    n = metrics.success_count + metrics.error_count
    if n == 1:
        metrics.latency_p50 = latency
        metrics.latency_p95 = latency
        metrics.latency_p99 = latency
        return
    p50 = metrics.latency_p50 * (n - 1) / n + latency / n
    p95 = metrics.latency_p95 * (n - 1) / n + latency / n
    p99 = metrics.latency_p99 * (n - 1) / n + latency / n
    metrics.latency_p50 = round(p50, 3)
    metrics.latency_p95 = round(p95, 3)
    metrics.latency_p99 = round(p99, 3)


def register_default_providers() -> None:
    from apps.backend.app.core.settings import settings

    is_homologation = settings.PROVIDER_MODE == "homologation"

    providers_config = [
        # --- MOCK_LIVE (ou HOMOLOGATION se modo homologation) ---
        ("multicaixa",   ProviderCapability.PAYMENT,
         ProviderStatus.HOMOLOGATION if is_homologation else ProviderStatus.MOCK_LIVE, "multicaixa",   "SILA Payment Team"),
        ("agt",          ProviderCapability.TAX_VERIFICATION,
         ProviderStatus.HOMOLOGATION if is_homologation else ProviderStatus.MOCK_LIVE, "agt",          "SILA Tax Team"),
        ("xroad_bi",     ProviderCapability.IDENTITY_VERIFICATION,
         ProviderStatus.HOMOLOGATION if is_homologation else ProviderStatus.MOCK_LIVE, "xroad_bi",     "SILA Identity Team"),
        ("registo_civil",ProviderCapability.CIVIL_REGISTRY,
         ProviderStatus.HOMOLOGATION if is_homologation else ProviderStatus.MOCK_LIVE, "registo_civil","SILA Civil Registry Team"),
        # --- REAL (credenciais ativas) ---
        ("emis",              ProviderCapability.EDUCATION_SYNC,  ProviderStatus.REAL, "emis",              "SILA Education Team"),
        ("tcu",               ProviderCapability.AUDIT,           ProviderStatus.REAL, "tcu",               "SILA Audit Team"),
        ("financas_publicas", ProviderCapability.FINANCIAL,       ProviderStatus.REAL, "financas_publicas", "SILA Treasury Team"),
        ("anatel",            ProviderCapability.TELECOM,         ProviderStatus.REAL, "anatel",            "SILA Telecom Team"),
    ]
    for name, cap, status, env, owner in providers_config:
        mock_reason = None
        if status == ProviderStatus.MOCK:
            mock_reason = "Sem credenciais configuradas (registo padrão)"
        elif status == ProviderStatus.MOCK_LIVE:
            mock_reason = "MOCK ao vivo — sem chaves reais"
        elif status == ProviderStatus.HOMOLOGATION:
            mock_reason = "Homologação institucional — ambiente de staging"
        ProviderRegistry.register(name, cap, status=status, version="0.1.0",
                                   environment=env, owner=owner, mock_reason=mock_reason)


__all__ = ["ProviderRegistry", "register_default_providers"]
