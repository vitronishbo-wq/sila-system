"""
Domain layer: Trust Score model with 40/40/20 evaluation logic.
Implements sovereign trust assessment for access control.
"""

from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk assessment based on trust score thresholds."""
    VOTING_GRADE = "VOTING_GRADE"           # >= 0.95 (high-assurance, voting eligible)
    LOW_RISK = "LOW_RISK"                   # >= 0.80 (standard auth)
    MEDIUM_RISK = "MEDIUM_RISK"             # >= 0.60 (MFA required)
    HIGH_RISK = "HIGH_RISK"                 # >= 0.40 (intensive MFA)
    CRITICAL_RISK = "CRITICAL_RISK"         # < 0.40 (BLOCK_ACCESS)


class TrustScore(BaseModel):
    """
    Sovereign Trust Engine: 40/40/20 trust assessment.
    
    Components:
    - Device Score (40%): Trusted device registry + authentication history
    - Biometric Score (40%): Fingerprint/face/iris confidence
    - Behavior Score (20%): Login pattern analysis + anomaly detection
    
    Formula: (device × 0.4) + (biometric × 0.4) + (behavior × 0.2)
    """

    device_score: float = Field(
        ge=0.0, le=1.0,
        description="Device trust score (trusted registry + auth history)"
    )
    biometric_score: float = Field(
        ge=0.0, le=1.0,
        description="Biometric confidence (fingerprint/face/iris match)"
    )
    behavior_score: float = Field(
        ge=0.0, le=1.0,
        description="Behavior analysis score (login patterns + anomaly)"
    )

    def calculate_total(self) -> float:
        """
        Calculate total trust score using 40/40/20 weighted model.
        
        Returns:
            float: Total score in [0.0, 1.0]
        """
        return (
            (self.device_score * 0.4) +
            (self.biometric_score * 0.4) +
            (self.behavior_score * 0.2)
        )

    def get_risk_level(self) -> RiskLevel:
        """
        Determine risk level from total score.
        
        Returns:
            RiskLevel: One of VOTING_GRADE, LOW_RISK, MEDIUM_RISK, HIGH_RISK, CRITICAL_RISK
        """
        total = self.calculate_total()

        if total >= 0.95:
            return RiskLevel.VOTING_GRADE
        elif total >= 0.80:
            return RiskLevel.LOW_RISK
        elif total >= 0.60:
            return RiskLevel.MEDIUM_RISK
        elif total >= 0.40:
            return RiskLevel.HIGH_RISK
        else:
            return RiskLevel.CRITICAL_RISK

    def requires_mfa(self) -> bool:
        """
        Check if multifactor authentication is required.
        MFA required for MEDIUM_RISK and above.
        
        Returns:
            bool: True if MFA required
        """
        risk_level = self.get_risk_level()
        return risk_level in {RiskLevel.MEDIUM_RISK, RiskLevel.HIGH_RISK, RiskLevel.CRITICAL_RISK}

    def block_access(self) -> bool:
        """
        Check if access should be blocked.
        Block only at CRITICAL_RISK level.
        
        Returns:
            bool: True if access should be blocked
        """
        return self.get_risk_level() == RiskLevel.CRITICAL_RISK
