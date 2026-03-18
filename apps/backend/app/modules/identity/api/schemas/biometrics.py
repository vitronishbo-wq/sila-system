"""
Pydantic schemas for biometric enrollment endpoints.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class BiometricEnrollRequest(BaseModel):
    """Request schema for biometric enrollment."""
    citizen_id: str = Field(..., description="Citizen identifier")
    biometric_type: str = Field(..., description="Biometric type (FINGERPRINT, FACE_RECOGNITION, IRIS, VOICE)")
    biometric_data: str = Field(..., description="Base64-encoded biometric payload")
    quality_score: float = Field(..., ge=0, le=100, description="Quality score (0-100)")
    quality_threshold: float | None = Field(default=None, ge=0, le=100, description="Minimum acceptable score")
    device_id: str | None = Field(default=None, description="Capture device identifier")
    location: str | None = Field(default=None, description="Capture location")


class BiometricEnrollResponse(BaseModel):
    """Response schema for biometric enrollment."""
    id: str
    citizen_id: str
    status: str
    created_at: datetime
