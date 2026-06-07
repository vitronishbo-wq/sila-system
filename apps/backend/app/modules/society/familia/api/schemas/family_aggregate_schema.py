from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apps.backend.app.modules.society.familia.domain.enums import FamilyStatus, MemberRole


class FamilyMemberCreateSchema(BaseModel):
    citizen_id: UUID
    role: MemberRole = Field(default=MemberRole.MEMBER)

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: MemberRole) -> MemberRole:
        if value == MemberRole.HEAD:
            raise ValueError("Papel HEAD e reservado a criacao do agregado")
        return value


class FamilyAggregateCreateSchema(BaseModel):
    head_citizen_id: UUID
    members: list[FamilyMemberCreateSchema] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class FamilyAggregateResponseSchema(BaseModel):
    id: UUID
    code: str
    head_citizen_id: UUID
    status: FamilyStatus
    member_count: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FamilyTransferHeadSchema(BaseModel):
    new_head_citizen_id: UUID


class FamilyDissolveSchema(BaseModel):
    reason: str = Field(min_length=2, max_length=200)


class FamilyMemberViewSchema(BaseModel):
    citizen_id: UUID
    role: MemberRole
    joined_at: datetime
    left_at: datetime | None = None
    is_active: bool
    citizen_name: str | None = None


class FamilyTreeResponseSchema(BaseModel):
    id: UUID
    code: str
    head_citizen_id: UUID
    status: FamilyStatus
    created_at: datetime
    updated_at: datetime
    members: list[FamilyMemberViewSchema]
    dependents: list[FamilyMemberViewSchema]
    model_config = ConfigDict(from_attributes=True)
