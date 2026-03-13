from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from apps.backend.app.modules.society.patrimonio_cultural.domain.enums import ActionType, AssetType, ClassificationLevel

class CulturalAssetCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    asset_type: AssetType
    province: str = Field(..., min_length=2, max_length=100)
    municipality: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    altitude: float | None = None
    address: str | None = None
    description: str | None = Field(default=None, max_length=2000)
    historical_period: str | None = None
    cultural_significance: str | None = None
    legal_reference: str | None = None

class ClassificationRequestSchema(BaseModel):
    classification_level: ClassificationLevel
    authority: str
    classification_date: datetime | None = None
    certificate_number: str | None = None
    legal_basis: str | None = None

    @field_validator('authority')
    @classmethod
    def validate_authority(cls, value: str) -> str:
        valid = {'MinCultura', 'UNESCO', 'Governo Provincial', 'Municipio'}
        if value not in valid:
            raise ValueError(f'Autoridade deve ser uma de: {sorted(valid)}')
        return value

class PreservationActionSchema(BaseModel):
    action_type: ActionType
    description: str = Field(..., min_length=10, max_length=2000)
    executed_by: str = Field(..., min_length=3, max_length=200)
    action_date: datetime | None = None
    cost: float | None = Field(default=None, ge=0)
    funding_source: str | None = None

class CulturalEventSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    event_date: datetime
    organizer: str = Field(..., min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    expected_attendance: int | None = Field(default=None, ge=0)
    requires_authorization: bool = False

class CulturalAssetResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    asset_id: UUID
    name: str
    asset_type: str
    province: str | None
    municipality: str | None
    location: dict
    status: str
    classification_level: str | None
    classification_date: datetime | None
    historical_period: str | None
    is_protected: bool
    has_unesco_classification: bool
    created_at: datetime