from dataclasses import dataclass
from typing import Any


@dataclass
class AcademicRecord:
    student_id: str
    current_class: str
    completed_classes: list[str]
    sanctions: list[str]
    debts: list[dict[str, Any]]

    def has_pending_debt(self) -> bool:
        return len(self.debts) > 0

    def has_sanctions(self) -> bool:
        return len(self.sanctions) > 0
