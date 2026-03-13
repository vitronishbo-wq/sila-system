from dataclasses import dataclass

@dataclass(slots=True)
class FailurePolicy:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    success_threshold: int = 3

    def __post_init__(self) -> None:
        if self.failure_threshold <= 0:
            raise ValueError('failure_threshold must be > 0')
        if self.recovery_timeout <= 0:
            raise ValueError('recovery_timeout must be > 0')
        if self.success_threshold <= 0:
            raise ValueError('success_threshold must be > 0')