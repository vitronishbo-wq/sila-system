import os
from dataclasses import dataclass

from .policy import FailurePolicy


@dataclass(slots=True)
class ResilienceConfig:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    success_threshold: int = 3

    @classmethod
    def from_env(cls, prefix: str = "SILA_CB_") -> "ResilienceConfig":
        return cls(
            failure_threshold=int(os.getenv(f"{prefix}FAILURE_THRESHOLD", "5")),
            recovery_timeout=float(os.getenv(f"{prefix}RECOVERY_TIMEOUT", "30")),
            success_threshold=int(os.getenv(f"{prefix}SUCCESS_THRESHOLD", "3")),
        )


def build_policy(config: ResilienceConfig | None = None) -> FailurePolicy:
    cfg = config or ResilienceConfig.from_env()
    return FailurePolicy(
        failure_threshold=cfg.failure_threshold,
        recovery_timeout=cfg.recovery_timeout,
        success_threshold=cfg.success_threshold,
    )
