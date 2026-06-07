from dataclasses import dataclass, field
from typing import Any


@dataclass
class TransferRequest:
    student_id: str
    target_school_id: str
    target_class: str | None
    academic_year: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TransferResult:
    eligible: bool
    score: int
    reasons: list | None
    automatic_execution: bool = False
