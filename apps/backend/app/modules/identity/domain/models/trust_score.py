"""Identity Trust Score domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.backend.app.modules.identity.domain.models.enums import TrustLevel


@dataclass
class TrustScore:
    """Domain model for Citizen Trust Score."""

    id: str
    citizen_id: str
    score: float
    level: TrustLevel = TrustLevel.LOW
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize after construction."""
        self._update_level()

    def _update_level(self):
        """Update trust level based on score."""
        if self.score >= 80:
            self.level = TrustLevel.VERIFIED
        elif self.score >= 60:
            self.level = TrustLevel.HIGH
        elif self.score >= 40:
            self.level = TrustLevel.MEDIUM
        else:
            self.level = TrustLevel.LOW

    def update_score(self, new_score: float, reason: str = "") -> dict[str, Any]:
        """Update trust score."""
        if new_score < 0 or new_score > 100:
            raise ValueError("Trust score must be between 0 and 100")
        old_score = self.score
        old_level = self.level
        self.score = new_score
        self._update_level()
        self.updated_at = datetime.utcnow()
        self.metadata["score_change_reason"] = reason
        return {
            "entity_type": "TRUST_SCORE",
            "entity_id": self.id,
            "action": "TRUST_SCORE_UPDATED",
            "previous_state": {"score": old_score, "level": old_level.value},
            "new_state": {"score": new_score, "level": self.level.value},
            "timestamp": self.updated_at,
        }
