from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


class AlertRuleType(Enum):
    OFFLINE = "offline"
    LATENCY = "latency"
    ERROR_RATE = "error_rate"
    RECONCILIATION_DIVERGENCE = "reconciliation_divergence"
    SLA_BREACH = "sla_breach"


@dataclass
class AlertRule:
    name: str
    rule_type: AlertRuleType
    enabled: bool = True
    severity: str = "warning"
    threshold: float = 0.0
    cooldown_minutes: int = 15
    description: str = ""
    evaluator: Optional[Callable] = None


class AlertRules:
    def __init__(self):
        self._rules: list[AlertRule] = [
            AlertRule(
                name="provider_offline",
                rule_type=AlertRuleType.OFFLINE,
                severity="critical",
                threshold=0.0,
                description="Provider status is not REAL and not available",
            ),
            AlertRule(
                name="latency_p95_breach",
                rule_type=AlertRuleType.LATENCY,
                severity="warning",
                threshold=1000.0,
                description="P95 latency exceeds 1000ms threshold",
            ),
            AlertRule(
                name="error_rate_high",
                rule_type=AlertRuleType.ERROR_RATE,
                severity="critical",
                threshold=0.05,
                description="Error rate exceeds 5% threshold",
            ),
            AlertRule(
                name="reconciliation_divergence",
                rule_type=AlertRuleType.RECONCILIATION_DIVERGENCE,
                severity="warning",
                threshold=1,
                description="Reconciliation divergences detected",
            ),
            AlertRule(
                name="sla_breach",
                rule_type=AlertRuleType.SLA_BREACH,
                severity="critical",
                threshold=0.0,
                description="SLA status is BREACHED",
            ),
        ]

    @property
    def rules(self) -> list[AlertRule]:
        return list(self._rules)

    def get(self, name: str) -> Optional[AlertRule]:
        for r in self._rules:
            if r.name == name:
                return r
        return None

    def add(self, rule: AlertRule) -> None:
        self._rules.append(rule)

    def remove(self, name: str) -> bool:
        before = len(self._rules)
        self._rules = [r for r in self._rules if r.name != name]
        return len(self._rules) < before

    def enable(self, name: str) -> bool:
        rule = self.get(name)
        if rule:
            rule.enabled = True
            return True
        return False

    def disable(self, name: str) -> bool:
        rule = self.get(name)
        if rule:
            rule.enabled = False
            return True
        return False

    def to_dict(self) -> list[dict]:
        return [
            {
                "name": r.name,
                "type": r.rule_type.value,
                "enabled": r.enabled,
                "severity": r.severity,
                "threshold": r.threshold,
                "description": r.description,
            }
            for r in self._rules
        ]
