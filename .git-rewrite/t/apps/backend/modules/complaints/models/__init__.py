"""Models for the complaints module."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ComplaintBase(BaseModel):
    """Base model for complaints."""

    title: str
    description: str
    category_id: Optional[int] = None


class ComplaintCreate(ComplaintBase):
    """Model for creating a complaint."""

    author_id: int


class ComplaintUpdate(ComplaintBase):
    """Model for updating a complaint."""

    status: Optional[str] = None


class ComplaintResponse(ComplaintBase):
    """Model for complaint responses."""

    id: int
    author_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ComplaintFilter(BaseModel):
    """Model for filtering complaints."""

    category_id: Optional[int] = None
    author_id: Optional[int] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ComplaintStats(BaseModel):
    """Model for complaint statistics."""

    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    by_category: dict[str, int]
    avg_resolution_time: float


class ComplaintCategoryBase(BaseModel):
    """Base model for complaint categories."""

    name: str


class ComplaintCategoryCreate(ComplaintCategoryBase):
    """Model for creating a complaint category."""


class ComplaintCategoryUpdate(ComplaintCategoryBase):
    """Model for updating a complaint category."""


class ComplaintCategoryResponse(ComplaintCategoryBase):
    """Model for complaint category responses."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class ComplaintCommentBase(BaseModel):
    """Base model for complaint comments."""

    text: str


class ComplaintCommentCreate(ComplaintCommentBase):
    """Model for creating a complaint comment."""

    complaint_id: int
    author_id: int


class ComplaintCommentResponse(ComplaintCommentBase):
    """Model for complaint comment responses."""

    id: int
    complaint_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
