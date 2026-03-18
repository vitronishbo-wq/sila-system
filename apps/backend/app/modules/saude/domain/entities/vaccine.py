from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class VaccineDose:
    id: UUID = field(default_factory=uuid4)
    citizen_id: UUID = field(default_factory=uuid4)
    vaccine_id: UUID = field(default_factory=uuid4)
    health_unit_id: UUID = field(default_factory=uuid4)
    applied_by: UUID = field(default_factory=uuid4)
    dose_number: int = 1
    batch_number: str = ''
    application_date: date = field(default_factory=date.today)
    next_dose_date: Optional[date] = None
    adverse_reactions: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def schedule_next_dose(self, next_date: date) -> None:
        self.next_dose_date = next_date

    def record_reaction(self, reaction: str) -> None:
        self.adverse_reactions = reaction