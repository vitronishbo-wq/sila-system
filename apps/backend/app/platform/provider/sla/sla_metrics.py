from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class SLAStatus(Enum):
    COMPLIANT = "compliant"
    WARNING = "warning"
    BREACHED = "breached"
    UNKNOWN = "unknown"


@dataclass
class SLAMetrics:
    provider: str
    availability: float = 0.0
    uptime_ms: float = 0.0
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    mttr_ms: float = 0.0
    mtbf_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    error_rate: float = 0.0
    last_failure: Optional[datetime] = None
    last_success: Optional[datetime] = None
    period_start: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    period_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sla_target_availability: float = 99.5
    sla_target_p95: float = 1000.0
    status: SLAStatus = SLAStatus.UNKNOWN

    def compute_status(self) -> SLAStatus:
        if self.availability >= self.sla_target_availability and self.p95_ms <= self.sla_target_p95:
            self.status = SLAStatus.COMPLIANT
        elif self.availability >= self.sla_target_availability or self.p95_ms <= self.sla_target_p95:
            self.status = SLAStatus.WARNING
        elif self.availability == 0.0 and self.total_requests == 0:
            self.status = SLAStatus.UNKNOWN
        else:
            self.status = SLAStatus.BREACHED
        return self.status

    def to_dict(self) -> dict:
        self.compute_status()
        return {
            "provider": self.provider,
            "availability": round(self.availability, 4),
            "uptime_ms": round(self.uptime_ms, 2),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "error_rate": round(self.error_rate, 4),
            "mttr_ms": round(self.mttr_ms, 2),
            "mtbf_ms": round(self.mtbf_ms, 2),
            "p50_ms": round(self.p50_ms, 2),
            "p95_ms": round(self.p95_ms, 2),
            "p99_ms": round(self.p99_ms, 2),
            "last_failure": self.last_failure.isoformat() if self.last_failure else None,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "sla_target_availability": self.sla_target_availability,
            "sla_target_p95_ms": self.sla_target_p95,
            "status": self.status.value,
        }
