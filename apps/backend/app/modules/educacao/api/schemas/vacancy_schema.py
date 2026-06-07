from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class VacancyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    institution: str
    grade: str
    available_slots: int
