from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RiskLevel(StrEnum):
    CRITICAL_RISK = "critical_risk"
    HIGH_RISK = "high_risk"
    MEDIUM_RISK = "medium_risk"
    LOW_RISK = "low_risk"


@dataclass(frozen=True)
class TrustScore:
    device_score: float
    biometric_score: float
    behavior_score: float

    def calculate_total(self) -> float:
        total = self.device_score * 0.4 + self.biometric_score * 0.4 + self.behavior_score * 0.2
        return max(0.0, min(1.0, total))

    def get_risk_level(self) -> RiskLevel:
        score = self.calculate_total()
        if score < 0.4:
            return RiskLevel.CRITICAL_RISK
        if score < 0.6:
            return RiskLevel.HIGH_RISK
        if score < 0.8:
            return RiskLevel.MEDIUM_RISK
        return RiskLevel.LOW_RISK

    def block_access(self) -> bool:
        return self.get_risk_level() == RiskLevel.CRITICAL_RISK
