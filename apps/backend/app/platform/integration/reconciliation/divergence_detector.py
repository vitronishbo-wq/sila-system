from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class DivergenceType(Enum):
    MISSING_INTERNAL = "missing_internal"
    MISSING_PROVIDER = "missing_provider"
    AMOUNT_MISMATCH = "amount_mismatch"
    STATUS_MISMATCH = "status_mismatch"
    TIMESTAMP_MISMATCH = "timestamp_mismatch"


@dataclass
class Divergence:
    divergence_type: DivergenceType
    reference: str
    internal_value: Optional[Any] = None
    provider_value: Optional[Any] = None
    description: str = ""
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "type": self.divergence_type.value,
            "reference": self.reference,
            "internal": str(self.internal_value) if self.internal_value is not None else None,
            "provider": str(self.provider_value) if self.provider_value is not None else None,
            "description": self.description,
            "detected_at": self.detected_at.isoformat(),
        }


class DivergenceDetector:
    def detect_missing_internal(self, provider_refs: set, internal_refs: set) -> list:
        divergences = []
        for ref in provider_refs - internal_refs:
            divergences.append(Divergence(
                divergence_type=DivergenceType.MISSING_INTERNAL,
                reference=ref,
                description=f"Transaction exists in provider but not in internal records: {ref}",
            ))
        return divergences

    def detect_missing_provider(self, internal_refs: set, provider_refs: set) -> list:
        divergences = []
        for ref in internal_refs - provider_refs:
            divergences.append(Divergence(
                divergence_type=DivergenceType.MISSING_PROVIDER,
                reference=ref,
                description=f"Transaction exists internally but not in provider records: {ref}",
            ))
        return divergences

    def detect_amount_mismatch(self, common_refs: set, internal_amounts: dict, provider_amounts: dict) -> list:
        divergences = []
        for ref in common_refs:
            ia = internal_amounts.get(ref, 0.0)
            pa = provider_amounts.get(ref, 0.0)
            if abs(ia - pa) > 0.01:
                divergences.append(Divergence(
                    divergence_type=DivergenceType.AMOUNT_MISMATCH,
                    reference=ref,
                    internal_value=ia,
                    provider_value=pa,
                    description=f"Amount mismatch: internal={ia}, provider={pa}",
                ))
        return divergences

    def detect_status_mismatch(self, common_refs: set, internal_statuses: dict, provider_statuses: dict) -> list:
        divergences = []
        for ref in common_refs:
            istatus = internal_statuses.get(ref, "")
            pstatus = provider_statuses.get(ref, "")
            if istatus != pstatus:
                divergences.append(Divergence(
                    divergence_type=DivergenceType.STATUS_MISMATCH,
                    reference=ref,
                    internal_value=istatus,
                    provider_value=pstatus,
                    description=f"Status mismatch: internal={istatus}, provider={pstatus}",
                ))
        return divergences

    def detect_all(self, internal_refs: set, provider_refs: set, internal_amounts: dict, provider_amounts: dict, internal_statuses: dict, provider_statuses: dict) -> list:
        divergences = []
        divergences.extend(self.detect_missing_internal(provider_refs, internal_refs))
        divergences.extend(self.detect_missing_provider(internal_refs, provider_refs))
        common = internal_refs & provider_refs
        divergences.extend(self.detect_amount_mismatch(common, internal_amounts, provider_amounts))
        divergences.extend(self.detect_status_mismatch(common, internal_statuses, provider_statuses))
        return divergences
