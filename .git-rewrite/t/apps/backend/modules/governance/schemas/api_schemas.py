"""
Governance module API schemas based on OpenAPI specification.

These schemas are used for Governance module endpoints and follow the OpenAPI contract.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import Field

from modules.common.bases import BaseSchema

# ============================================================================
# Institution Schemas
# ============================================================================


class InstitutionCreate(BaseSchema):
    """Schema for creating an institution."""

    name: str = Field(..., description="Institution name", max_length=200)
    acronym: Optional[str] = Field(
        None, description="Institution acronym", max_length=50
    )
    institution_type: Optional[str] = Field(
        None,
        description="Type of institution (ministry, agency, department, etc.)",
        max_length=100,
    )
    jurisdiction: Optional[str] = Field(
        None, description="Jurisdiction", max_length=200
    )
    description: Optional[str] = Field(
        None, description="Institution description", max_length=2000
    )
    founding_date: Optional[datetime] = Field(None, description="Founding date")
    website: Optional[str] = Field(
        None, description="Institution website", max_length=200
    )
    contact_info: Optional[Dict[str, Any]] = Field(
        None, description="Contact information (JSON)"
    )
    leadership: Optional[Dict[str, Any]] = Field(
        None, description="Leadership information (JSON)"
    )
    parent_institution_id: Optional[UUID] = Field(
        None, description="Parent institution ID"
    )


class InstitutionUpdate(BaseSchema):
    """Schema for updating an institution."""

    name: Optional[str] = Field(None, description="Institution name", max_length=200)
    acronym: Optional[str] = Field(
        None, description="Institution acronym", max_length=50
    )
    institution_type: Optional[str] = Field(
        None, description="Type of institution", max_length=100
    )
    jurisdiction: Optional[str] = Field(
        None, description="Jurisdiction", max_length=200
    )
    description: Optional[str] = Field(
        None, description="Institution description", max_length=2000
    )
    website: Optional[str] = Field(
        None, description="Institution website", max_length=200
    )
    contact_info: Optional[Dict[str, Any]] = Field(
        None, description="Contact information (JSON)"
    )
    leadership: Optional[Dict[str, Any]] = Field(
        None, description="Leadership information (JSON)"
    )


class InstitutionResponse(BaseSchema):
    """Schema for institution response."""

    id: UUID = Field(..., description="Institution unique identifier")
    name: str = Field(..., description="Institution name")
    acronym: Optional[str] = Field(None, description="Institution acronym")
    institution_type: Optional[str] = Field(None, description="Type of institution")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction")
    description: Optional[str] = Field(None, description="Institution description")
    founding_date: Optional[datetime] = Field(None, description="Founding date")
    website: Optional[str] = Field(None, description="Institution website")
    contact_info: Optional[Dict[str, Any]] = Field(
        None, description="Contact information"
    )
    leadership: Optional[Dict[str, Any]] = Field(
        None, description="Leadership information"
    )
    parent_institution_id: Optional[UUID] = Field(
        None, description="Parent institution ID"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class InstitutionsListResponse(BaseSchema):
    """Schema for list of institutions response."""

    items: List[InstitutionResponse] = Field(
        default_factory=list, description="List of institutions"
    )
    total: int = Field(
        ...,
        description="Total number of institutions",
        json_schema_extra={"example": 0},
    )


# ============================================================================
# Mandate Schemas
# ============================================================================


class MandateCreate(BaseSchema):
    """Schema for creating a mandate."""

    title: str = Field(..., description="Mandate title", max_length=200)
    description: Optional[str] = Field(
        None, description="Mandate description", max_length=2000
    )
    mandate_type: Optional[str] = Field(
        None,
        description="Type of mandate (executive, legislative, judicial, etc.)",
        max_length=100,
    )
    issuing_authority: Optional[str] = Field(
        None, description="Issuing authority", max_length=200
    )
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    status: str = Field(
        default="active", description="Mandate status (active, expired, revoked)"
    )
    scope: Optional[Dict[str, Any]] = Field(
        None, description="Scope and limitations (JSON)"
    )
    related_documents: Optional[Dict[str, Any]] = Field(
        None, description="Related documents (JSON)"
    )
    institution_id: Optional[UUID] = Field(None, description="Related institution ID")


class MandateUpdate(BaseSchema):
    """Schema for updating a mandate."""

    title: Optional[str] = Field(None, description="Mandate title", max_length=200)
    description: Optional[str] = Field(
        None, description="Mandate description", max_length=2000
    )
    status: Optional[str] = Field(None, description="Mandate status")
    end_date: Optional[datetime] = Field(None, description="End date")


class MandateResponse(BaseSchema):
    """Schema for mandate response."""

    id: UUID = Field(..., description="Mandate unique identifier")
    title: str = Field(..., description="Mandate title")
    description: Optional[str] = Field(None, description="Mandate description")
    mandate_type: Optional[str] = Field(None, description="Type of mandate")
    issuing_authority: Optional[str] = Field(None, description="Issuing authority")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    status: str = Field(..., description="Mandate status")
    scope: Optional[Dict[str, Any]] = Field(None, description="Scope and limitations")
    related_documents: Optional[Dict[str, Any]] = Field(
        None, description="Related documents"
    )
    institution_id: Optional[UUID] = Field(None, description="Related institution ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class MandatesListResponse(BaseSchema):
    """Schema for list of mandates response."""

    items: List[MandateResponse] = Field(
        default_factory=list, description="List of mandates"
    )
    total: int = Field(
        ..., description="Total number of mandates", json_schema_extra={"example": 0}
    )


# ============================================================================
# Decision Schemas
# ============================================================================


class DecisionCreate(BaseSchema):
    """Schema for creating a decision."""

    title: str = Field(..., description="Decision title", max_length=200)
    description: Optional[str] = Field(
        None, description="Decision description", max_length=1000
    )
    decision_type: Optional[str] = Field(
        None,
        description="Type of decision (policy, resolution, directive, etc.)",
        max_length=100,
    )
    status: str = Field(
        default="proposed",
        description="Decision status (proposed, approved, rejected, implemented)",
    )
    voting_record: Optional[Dict[str, Any]] = Field(
        None, description="Voting record (JSON)"
    )
    meeting_id: Optional[UUID] = Field(None, description="Related council meeting ID")
    effective_date: Optional[datetime] = Field(None, description="Effective date")
    expiration_date: Optional[datetime] = Field(None, description="Expiration date")
    related_documents: Optional[Dict[str, Any]] = Field(
        None, description="Related documents (JSON)"
    )


class DecisionUpdate(BaseSchema):
    """Schema for updating a decision."""

    title: Optional[str] = Field(None, description="Decision title", max_length=200)
    description: Optional[str] = Field(
        None, description="Decision description", max_length=1000
    )
    status: Optional[str] = Field(None, description="Decision status")
    voting_record: Optional[Dict[str, Any]] = Field(
        None, description="Voting record (JSON)"
    )


class DecisionResponse(BaseSchema):
    """Schema for decision response."""

    id: UUID = Field(..., description="Decision unique identifier")
    title: str = Field(..., description="Decision title")
    description: Optional[str] = Field(None, description="Decision description")
    decision_type: Optional[str] = Field(None, description="Type of decision")
    status: str = Field(..., description="Decision status")
    voting_record: Optional[Dict[str, Any]] = Field(None, description="Voting record")
    meeting_id: Optional[UUID] = Field(None, description="Related council meeting ID")
    effective_date: Optional[datetime] = Field(None, description="Effective date")
    expiration_date: Optional[datetime] = Field(None, description="Expiration date")
    related_documents: Optional[Dict[str, Any]] = Field(
        None, description="Related documents"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class DecisionsListResponse(BaseSchema):
    """Schema for list of decisions response."""

    items: List[DecisionResponse] = Field(
        default_factory=list, description="List of decisions"
    )
    total: int = Field(
        ..., description="Total number of decisions", json_schema_extra={"example": 0}
    )


# ============================================================================
# Council Meeting Schemas
# ============================================================================


class CouncilMeetingCreate(BaseSchema):
    """Schema for creating a council meeting."""

    title: str = Field(..., description="Meeting title", max_length=200)
    description: Optional[str] = Field(
        None, description="Meeting description", max_length=1000
    )
    location: Optional[str] = Field(
        None, description="Meeting location", max_length=200
    )
    start_time: datetime = Field(..., description="Start time")
    end_time: Optional[datetime] = Field(None, description="End time")
    status: str = Field(
        default="scheduled",
        description="Meeting status (scheduled, in_progress, completed, canceled)",
    )
    agenda: Optional[Dict[str, Any]] = Field(None, description="Meeting agenda (JSON)")
    minutes: Optional[Dict[str, Any]] = Field(
        None, description="Meeting minutes (JSON)"
    )
    decisions: Optional[Dict[str, Any]] = Field(
        None, description="Decisions made (JSON)"
    )
    participants: Optional[Dict[str, Any]] = Field(
        None, description="Participants (JSON)"
    )
    council_id: Optional[UUID] = Field(None, description="Council ID")


class CouncilMeetingUpdate(BaseSchema):
    """Schema for updating a council meeting."""

    title: Optional[str] = Field(None, description="Meeting title", max_length=200)
    description: Optional[str] = Field(
        None, description="Meeting description", max_length=1000
    )
    status: Optional[str] = Field(None, description="Meeting status")
    end_time: Optional[datetime] = Field(None, description="End time")
    minutes: Optional[Dict[str, Any]] = Field(
        None, description="Meeting minutes (JSON)"
    )


class CouncilMeetingResponse(BaseSchema):
    """Schema for council meeting response."""

    id: UUID = Field(..., description="Meeting unique identifier")
    title: str = Field(..., description="Meeting title")
    description: Optional[str] = Field(None, description="Meeting description")
    location: Optional[str] = Field(None, description="Meeting location")
    start_time: datetime = Field(..., description="Start time")
    end_time: Optional[datetime] = Field(None, description="End time")
    status: str = Field(..., description="Meeting status")
    agenda: Optional[Dict[str, Any]] = Field(None, description="Meeting agenda")
    minutes: Optional[Dict[str, Any]] = Field(None, description="Meeting minutes")
    decisions: Optional[Dict[str, Any]] = Field(None, description="Decisions made")
    participants: Optional[Dict[str, Any]] = Field(None, description="Participants")
    council_id: Optional[UUID] = Field(None, description="Council ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class CouncilMeetingsListResponse(BaseSchema):
    """Schema for list of council meetings response."""

    items: List[CouncilMeetingResponse] = Field(
        default_factory=list, description="List of council meetings"
    )
    total: int = Field(
        ...,
        description="Total number of council meetings",
        json_schema_extra={"example": 0},
    )


__all__ = [
    # Institution schemas
    "InstitutionCreate",
    "InstitutionUpdate",
    "InstitutionResponse",
    "InstitutionsListResponse",
    # Mandate schemas
    "MandateCreate",
    "MandateUpdate",
    "MandateResponse",
    "MandatesListResponse",
    # Decision schemas
    "DecisionCreate",
    "DecisionUpdate",
    "DecisionResponse",
    "DecisionsListResponse",
    # Council Meeting schemas
    "CouncilMeetingCreate",
    "CouncilMeetingUpdate",
    "CouncilMeetingResponse",
    "CouncilMeetingsListResponse",
]
