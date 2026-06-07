from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VaccineDoseInput(BaseModel):
    citizen_id: UUID
    vaccine_id: UUID
    health_unit_id: UUID
    applied_by: UUID
    dose_number: int
    batch_number: str
    application_date: date
    next_dose_date: date | None = None
    adverse_reactions: str | None = None


class VaccineDoseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    citizen_id: UUID
    vaccine_id: UUID
    health_unit_id: UUID
    applied_by: UUID
    dose_number: int
    batch_number: str
    application_date: date
    next_dose_date: date | None
    adverse_reactions: str | None
