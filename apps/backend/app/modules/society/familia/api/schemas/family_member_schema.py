from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.modules.society.familia.domain.enums import MemberRole

class FamilyMemberSchema(BaseModel):
    id: UUID
    family_id: UUID
    citizen_id: UUID
    role: MemberRole
    joined_at: datetime
    left_at: datetime | None = None