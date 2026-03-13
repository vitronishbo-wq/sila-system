from datetime import date
from uuid import UUID
from pydantic import BaseModel
from apps.backend.app.modules.society.familia.domain.enums import RelationshipType

class RelationshipSchema(BaseModel):
    id: UUID
    citizen_a_id: UUID
    citizen_b_id: UUID
    relationship_type: RelationshipType
    start_date: date
    end_date: date | None = None