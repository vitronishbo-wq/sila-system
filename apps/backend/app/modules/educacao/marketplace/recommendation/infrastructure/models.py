"""SQLAlchemy models for Recommendation subdomain"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class UserPreferenceModel(Base):
    """Model for storing citizen marketplace preferences"""
    
    __tablename__ = "marketplace_user_preferences"
    
    # Identity
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    citizen_id: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    
    # Preferences
    preferred_levels: Mapped[Optional[list]] = mapped_column(
        JSONB, nullable=True, default=[]
    )
    preferred_modalities: Mapped[Optional[list]] = mapped_column(
        JSONB, nullable=True, default=[]
    )
    preferred_cities: Mapped[Optional[list]] = mapped_column(
        JSONB, nullable=True, default=[]
    )
    
    # Constraints
    price_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    distance_max_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Index for quick lookups by citizen
    __table_args__ = (
        Index("idx_marketplace_user_pref_citizen", "citizen_id", unique=True),
    )


class RecommendationModel(Base):
    """Model for storing generated recommendations"""
    
    __tablename__ = "marketplace_recommendations"
    
    # Identity
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    citizen_id: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    opportunity_id: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    
    # Recommendation data
    score: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    model_version: Mapped[str] = mapped_column(String(32), nullable=False)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Indices
    __table_args__ = (
        Index("idx_marketplace_rec_citizen", "citizen_id"),
        Index("idx_marketplace_rec_opportunity", "opportunity_id"),
        Index("idx_marketplace_rec_score", "score"),
    )
