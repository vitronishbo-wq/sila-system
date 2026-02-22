"""
Services module API schemas based on OpenAPI specification.

These schemas are used for Services module endpoints and follow the OpenAPI contract.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ServiceItem(BaseModel):
    """Schema for a single service item."""

    name: str = Field(
        ..., description="Service name", json_schema_extra={"example": "authentication"}
    )
    status: str = Field(
        ..., description="Service status", json_schema_extra={"example": "active"}
    )
    description: Optional[str] = Field(
        None,
        description="Service description",
        json_schema_extra={"example": "Authentication service"},
    )

    model_config = ConfigDict(from_attributes=True)


class ServicesListResponse(BaseModel):
    """Schema for services list response."""

    items: List[ServiceItem] = Field(
        default_factory=list, description="List of services"
    )
    total: int = Field(
        ..., description="Total number of services", json_schema_extra={"example": 0}
    )

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    "ServiceItem",
    "ServicesListResponse",
]
