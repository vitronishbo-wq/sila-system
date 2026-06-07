from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class ProviderStatus(Enum):
    REAL = "real"
    HOMOLOGATION = "homologation"
    MOCK = "mock"
    MOCK_LIVE = "mock_live"
    DISABLED = "disabled"


class ProviderCapability(Enum):
    IDENTITY_VERIFICATION = "identity_verification"
    TAX_VERIFICATION = "tax_verification"
    PAYMENT = "payment"
    ADDRESS_GEOCODING = "address_geocoding"
    DOCUMENT_VERIFICATION = "document_verification"
    CIVIL_REGISTRY = "civil_registry"
    EDUCATION_SYNC = "education_sync"
    INTEROPERABILITY = "interoperability"
    AUDIT = "audit"
    FINANCIAL = "financial"
    TELECOM = "telecom"


@dataclass
class ProviderMetrics:
    success_count: int = 0
    error_count: int = 0
    latency_p50: float = 0.0
    latency_p95: float = 0.0
    latency_p99: float = 0.0
    last_latency: float = 0.0
    last_success: Optional[datetime] = None
    last_error: Optional[datetime] = None
    last_error_message: Optional[str] = None

    @property
    def availability(self) -> float:
        total = self.success_count + self.error_count
        if total == 0:
            return 0.0
        return round(self.success_count / total * 100, 2)

    @property
    def success_rate(self) -> float:
        return self.availability

    @property
    def error_rate(self) -> float:
        total = self.success_count + self.error_count
        if total == 0:
            return 0.0
        return round(self.error_count / total * 100, 2)


@dataclass
class ProviderHealth:
    provider: str
    status: ProviderStatus
    capability: ProviderCapability
    metrics: ProviderMetrics = field(default_factory=ProviderMetrics)
    last_success: Optional[datetime] = None
    sla_target: Optional[float] = None
    version: str = "0.0.0"
    enabled: bool = True
    mock_reason: Optional[str] = None
    environment: str = "dev"
    owner: str = ""

    @property
    def healthy(self) -> bool:
        if not self.enabled:
            return True
        if self.status in (ProviderStatus.MOCK, ProviderStatus.MOCK_LIVE):
            return True
        return self.metrics.availability >= (self.sla_target or 0.0)

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "status": self.status.value,
            "capability": self.capability.value,
            "version": self.version,
            "enabled": self.enabled,
            "environment": self.environment,
            "owner": self.owner,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "availability": self.metrics.availability,
            "sla": f"{self.sla_target:.1%}" if self.sla_target is not None else "N/A",
            "success_rate": self.metrics.success_rate,
            "error_rate": self.metrics.error_rate,
            "mock_reason": self.mock_reason,
        }

    def to_health_dict(self) -> dict:
        return {
            "provider": self.provider,
            "status": self.status.value,
            "environment": self.environment,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "availability": self.metrics.availability,
            "sla": f"{self.sla_target:.1%}" if self.sla_target is not None else "N/A",
            "mock_reason": self.mock_reason,
        }
