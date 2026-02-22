"""
Base models and schemas for the SILA system.

This module provides abstract base models and schemas that define common patterns
used across all modules, ensuring consistency in data structures and validation.
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID

# Type variable for generic base classes
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


# SQLAlchemy Base Models
from core.db.base_class import Base  # Use centralized Base


class TimestampMixin(BaseModel):
    """Mixin for adding timestamp fields to models."""

    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )

    model_config = ConfigDict(from_attributes=True)


class UUIDMixin(BaseModel):
    """Mixin for adding UUID primary key to models."""

    id: UUID = Field(default_factory=uuid4, description="Unique identifier")

    model_config = ConfigDict(from_attributes=True)


class AuditMixin(BaseModel):
    """Mixin for adding audit fields to models."""

    created_by: Optional[str] = Field(None, description="User who created the record")
    updated_by: Optional[str] = Field(
        None, description="User who last updated the record"
    )
    version: int = Field(default=1, description="Version number for optimistic locking")

    model_config = ConfigDict(from_attributes=True)


# SQLAlchemy Base Model with common fields
class SILABase(Base):
    """Base SQLAlchemy model with common fields for all SILA entities."""

    __abstract__ = True

    id = Column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    version = Column(Integer, nullable=False, default=1)


# Pydantic Base Schemas
class BaseSchema(BaseModel):
    """Base Pydantic schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid",
    )


class BaseResponseSchema(BaseSchema):
    """Base schema for API responses."""

    id: UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime fields consistently."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v


class BaseCreateSchema(BaseSchema):
    """Base schema for creating entities."""

    created_by: Optional[str] = Field(None, description="User creating the entity")


class BaseUpdateSchema(BaseSchema):
    """Base schema for updating entities."""

    updated_by: Optional[str] = Field(None, description="User updating the entity")


class BaseListResponse(BaseSchema, Generic[ModelType]):
    """Base schema for paginated list responses."""

    items: List[ModelType] = Field(..., description="List of items")
    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, le=100, description="Page size")
    pages: int = Field(..., ge=0, description="Total number of pages")

    @classmethod
    def create(
        cls, items: List[ModelType], total: int, page: int, size: int
    ) -> "BaseListResponse[ModelType]":
        """Create a paginated response."""
        pages = (total + size - 1) // size  # Ceiling division
        return cls(items=items, total=total, page=page, size=size, pages=pages)


class BaseSearchSchema(BaseSchema):
    """Base schema for search parameters."""

    query: Optional[str] = Field(None, description="Search query")
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Page size")
    sort_by: Optional[str] = Field("created_at", description="Field to sort by")
    sort_order: Optional[str] = Field(
        "desc", pattern="^(asc|desc)$", description="Sort order"
    )

    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, v):
        """Validate sort order."""
        if v and v not in ["asc", "desc"]:
            raise ValueError("sort_order must be 'asc' or 'desc'")
        return v


class BaseFilterSchema(BaseSchema):
    """Base schema for filter parameters."""

    created_after: Optional[datetime] = Field(
        None, description="Filter by creation date after"
    )
    created_before: Optional[datetime] = Field(
        None, description="Filter by creation date before"
    )
    updated_after: Optional[datetime] = Field(
        None, description="Filter by update date after"
    )
    updated_before: Optional[datetime] = Field(
        None, description="Filter by update date before"
    )
    created_by: Optional[str] = Field(None, description="Filter by creator")
    updated_by: Optional[str] = Field(None, description="Filter by updater")

    @field_validator(
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
        mode="before",
    )
    @classmethod
    def parse_datetime_fields(cls, v):
        """Parse datetime filter fields."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v


class BaseOperationResponse(BaseSchema):
    """Base schema for operation responses."""

    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Operation message")
    data: Optional[Dict[str, Any]] = Field(
        None, description="Additional operation data"
    )

    @classmethod
    def success_response(
        cls, message: str, data: Optional[Dict[str, Any]] = None
    ) -> "BaseOperationResponse":
        """Create a success response."""
        return cls(success=True, message=message, data=data)

    @classmethod
    def error_response(
        cls, message: str, data: Optional[Dict[str, Any]] = None
    ) -> "BaseOperationResponse":
        """Create an error response."""
        return cls(success=False, message=message, data=data)


# Common field definitions
class CommonFields:
    """Common field definitions used across schemas."""

    ID_FIELD = Field(..., description="Unique identifier")
    TIMESTAMP_FIELD = Field(default_factory=datetime.utcnow, description="Timestamp")
    OPTIONAL_STRING_FIELD = Field(None, description="Optional string field")
    REQUIRED_STRING_FIELD = Field(..., description="Required string field")
    EMAIL_FIELD = Field(
        ...,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Email address",
    )
    PHONE_FIELD = Field(
        None, pattern=r"^\+?[1-9]\d{1,14}$", description="Phone number in E.164 format"
    )

    @staticmethod
    def enum_field(enum_class, description: str):
        """Create an enum field with description."""
        return Field(..., description=description)


# Export all base classes
__all__ = [
    # SQLAlchemy
    "Base",
    "SILABase",
    "TimestampMixin",
    "UUIDMixin",
    "AuditMixin",
    # Pydantic
    "BaseSchema",
    "BaseResponseSchema",
    "BaseCreateSchema",
    "BaseUpdateSchema",
    "BaseListResponse",
    "BaseSearchSchema",
    "BaseFilterSchema",
    "BaseOperationResponse",
    "CommonFields",
    # Type variables
    "ModelType",
    "CreateSchemaType",
    "UpdateSchemaType",
]
