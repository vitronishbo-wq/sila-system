"""
API Response schemas based on OpenAPI specification.

These schemas are used across all modules for consistent API responses.
"""

from datetime import datetime, timezone

from pydantic import Field, ConfigDict

from modules.common.bases.bases import BaseSchema


class RootResponse(BaseSchema):
    """Root endpoint response."""

    message: str = Field(
        ...,
        description="Welcome message",
        json_schema_extra={"example": "Welcome to SILA System API"},
    )
    status: str = Field(
        ..., description="System status", json_schema_extra={"example": "online"}
    )


class HealthCheckResponse(BaseSchema):
    """Health check response."""

    status: str = Field(
        ..., description="Health status", json_schema_extra={"example": "healthy"}
    )
    timestamp: datetime = Field(
        ...,
        description="Current timestamp",
        json_schema_extra={"example": "2025-01-05T10:00:00Z"},
    )


class SystemInfoResponse(BaseSchema):
    """System information response."""

    name: str = Field(
        ..., description="System name", json_schema_extra={"example": "SILA System"}
    )
    version: str = Field(
        ..., description="System version", json_schema_extra={"example": "1.0.0"}
    )
    environment: str = Field(
        ..., description="Environment", json_schema_extra={"example": "development"}
    )


class PingResponse(BaseSchema):
    """Ping response for module health checks."""

    message: str = Field(
        ..., description="Ping message", json_schema_extra={"example": "pong"}
    )
    timestamp: datetime = Field(
        ...,
        description="Current timestamp",
        json_schema_extra={"example": "2025-01-05T10:00:00Z"},
    )


class TrainingStatusResponse(BaseSchema):
    """Training module status response."""

    status: str = Field(
        ..., description="Module status", json_schema_extra={"example": "operational"}
    )
    module: str = Field(
        ..., description="Module name", json_schema_extra={"example": "training"}
    )
    timestamp: datetime = Field(
        ...,
        description="Current timestamp",
        json_schema_extra={"example": "2025-01-05T10:00:00Z"},
    )


class ErrorResponse(BaseSchema):
    """Standard error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: str | None = Field(None, description="Error details")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Error timestamp",
    )


class PaginationResponse(BaseSchema):
    """Pagination metadata for list responses."""

    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, le=100, description="Page size")
    pages: int = Field(..., ge=0, description="Total number of pages")


class SuccessResponse(BaseSchema):
    """Standard success response."""

    success: bool = Field(..., description="Operation status")
    message: str = Field(..., description="Success message")
    data: dict | None = Field(None, description="Response data")


__all__ = [
    "RootResponse",
    "HealthCheckResponse",
    "SystemInfoResponse",
    "PingResponse",
    "TrainingStatusResponse",
    "ErrorResponse",
    "PaginationResponse",
    "SuccessResponse",
]
