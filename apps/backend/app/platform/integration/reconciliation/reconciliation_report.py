from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class ReconciliationStatus(Enum):
    OK = "ok"
    DIVERGENCE_FOUND = "divergence_found"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ReconciliationReport:
    provider: str
    status: ReconciliationStatus
    internal_count: int = 0
    provider_count: int = 0
    matched_count: int = 0
    divergences: list[dict] = field(default_factory=list)
    total_amount_internal: float = 0.0
    total_amount_provider: float = 0.0
    error_message: Optional[str] = None
    scenario: str = "live"
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    duration_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "status": self.status.value,
            "internal_count": self.internal_count,
            "provider_count": self.provider_count,
            "matched_count": self.matched_count,
            "divergences": len(self.divergences),
            "divergence_details": self.divergences,
            "total_amount_internal": self.total_amount_internal,
            "total_amount_provider": self.total_amount_provider,
            "scenario": self.scenario,
            "error": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": round(self.duration_ms, 2),
        }
