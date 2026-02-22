# governance schemas module
# Import from api_schemas.py which has the complete OpenAPI-aligned schemas

from .api_schemas import (
    # Institution schemas
    InstitutionCreate,
    InstitutionUpdate,
    InstitutionResponse,
    InstitutionsListResponse,
    # Mandate schemas
    MandateCreate,
    MandateUpdate,
    MandateResponse,
    MandatesListResponse,
    # Council Meeting schemas
    CouncilMeetingCreate,
    CouncilMeetingUpdate,
    CouncilMeetingResponse,
    CouncilMeetingsListResponse,
    # Decision schemas
    DecisionCreate,
    DecisionUpdate,
    DecisionResponse,
    DecisionsListResponse,
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
    # Council Meeting schemas
    "CouncilMeetingCreate",
    "CouncilMeetingUpdate",
    "CouncilMeetingResponse",
    "CouncilMeetingsListResponse",
    # Decision schemas
    "DecisionCreate",
    "DecisionUpdate",
    "DecisionResponse",
    "DecisionsListResponse",
]
