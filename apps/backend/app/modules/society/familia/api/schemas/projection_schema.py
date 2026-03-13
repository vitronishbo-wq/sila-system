from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class FamilyCompositionProjectionSchema(BaseModel):
    family_id: UUID
    head_citizen_id: UUID
    member_count: int
    dependents_count: int
    composition_json: dict
    last_updated: datetime