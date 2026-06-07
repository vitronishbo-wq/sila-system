import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional

from apps.backend.app.platform.integration.provider_registry import ProviderRegistry
from apps.backend.app.platform.provider.alerting.alert_rules import AlertRules
from apps.backend.app.platform.provider.sla.sla_engine import SLAEngine

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Alert:
    rule_name: str
    provider: str
    severity: AlertSeverity
    message: str
    details: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    acknowledged: bool = False

    def to_dict(self) -> dict:
        return {
            "rule": self.rule_name,
            "provider": self.provider,
            "severity": self.severity.value,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "acknowledged": self.acknowledged,
        }


class AlertEngine:
    def __init__(self, sla_engine: Optional[SLAEngine] = None):
        self._rules = AlertRules()
        self._sla_engine = sla_engine or SLAEngine()
        self._alerts: list[Alert] = []
        self._cooldowns: dict[str, datetime] = {}

    @property
    def rules(self) -> AlertRules:
        return self._rules

    async def evaluate(self, slas: Optional[dict[str, Any]] = None) -> list[Alert]:
        new_alerts = []
        now = datetime.now(timezone.utc)

        for provider, health in ProviderRegistry.list_registered().items():
            for rule in self._rules.rules:
                if not rule.enabled:
                    continue
                cooldown_key = f"{rule.name}:{provider}"
                last_alert = self._cooldowns.get(cooldown_key)
                if last_alert and (now - last_alert) < timedelta(minutes=rule.cooldown_minutes):
                    continue
                alert = await self._evaluate_rule(rule, provider, health, slas, now)
                if alert:
                    new_alerts.append(alert)
                    self._alerts.append(alert)
                    self._cooldowns[cooldown_key] = now

        for a in new_alerts:
            logger.warning(f"alert rule={a.rule_name} provider={a.provider} severity={a.severity.value} message={a.message}")
        return new_alerts

    async def _evaluate_rule(self, rule, provider: str, health, slas, now) -> Optional[Alert]:
        from apps.backend.app.platform.integration.models import ProviderStatus

        if rule.rule_type.value == "offline":
            if health and health.status == ProviderStatus.MOCK:
                return Alert(
                    rule_name=rule.name,
                    provider=provider,
                    severity=AlertSeverity.CRITICAL,
                    message=f"Provider '{provider}' is running in MOCK mode",
                    details={"status": health.status.value, "capability": health.capability.value},
                )
            if health and not health.enabled:
                return Alert(
                    rule_name=rule.name,
                    provider=provider,
                    severity=AlertSeverity.CRITICAL,
                    message=f"Provider '{provider}' is disabled",
                    details={"enabled": False},
                )

        if rule.rule_type.value == "latency_p95_breach":
            sla = self._sla_engine.compute(provider)
            if sla and sla.p95_ms > rule.threshold:
                return Alert(
                    rule_name=rule.name,
                    provider=provider,
                    severity=AlertSeverity.WARNING,
                    message=f"Provider '{provider}' P95 latency {sla.p95_ms:.0f}ms exceeds {rule.threshold:.0f}ms threshold",
                    details={"p95_ms": sla.p95_ms, "threshold": rule.threshold},
                )

        if rule.rule_type.value == "error_rate_high":
            sla = self._sla_engine.compute(provider)
            if sla and sla.error_rate > rule.threshold:
                return Alert(
                    rule_name=rule.name,
                    provider=provider,
                    severity=AlertSeverity.CRITICAL,
                    message=f"Provider '{provider}' error rate {sla.error_rate:.2%} exceeds {rule.threshold:.0%} threshold",
                    details={"error_rate": sla.error_rate, "threshold": rule.threshold},
                )

        if rule.rule_type.value == "sla_breach":
            sla = self._sla_engine.compute(provider)
            if sla and sla.status.value == "breached":
                return Alert(
                    rule_name=rule.name,
                    provider=provider,
                    severity=AlertSeverity.CRITICAL,
                    message=f"Provider '{provider}' SLA BREACHED (availability={sla.availability:.1f}%)",
                    details={
                        "availability": sla.availability,
                        "sla_target": sla.sla_target_availability,
                        "status": sla.status.value,
                    },
                )

        return None

    def get_alerts(self, since: Optional[datetime] = None) -> list[Alert]:
        if since:
            return [a for a in self._alerts if a.timestamp >= since]
        return list(self._alerts)

    def acknowledge(self, index: int) -> bool:
        if 0 <= index < len(self._alerts):
            self._alerts[index].acknowledged = True
            return True
        return False

    def clear(self) -> None:
        self._alerts.clear()
        self._cooldowns.clear()
