"""SQLAlchemy models for Ranking subdomain"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Index,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class InstitutionMetricsModel(Base):
    """Model for storing institution metrics used in ranking"""
    
    __tablename__ = "marketplace_institution_metrics"
    
    # Identity
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    institution_id: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    institution_name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    
    # Quality metrics (0-100)
    quality_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reputation_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    accessibility_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    employment_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # Satisfaction (0-5)
    student_satisfaction: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # Institution data
    number_programs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_students: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    average_rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # Additional metrics as JSON
    custom_metrics: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Indices for ranking queries
    __table_args__ = (
        Index("idx_marketplace_metrics_inst", "institution_id", unique=True),
        Index("idx_marketplace_metrics_quality", "quality_score"),
        Index("idx_marketplace_metrics_reputation", "reputation_score"),
        Index("idx_marketplace_metrics_employment", "employment_rate"),
    )


class RankingSnapshotModel(Base):
    """Model for storing ranking snapshots for historical tracking"""
    
    __tablename__ = "marketplace_ranking_snapshots"
    
    # Identity
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # Ranking data
    rank_position: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    institution_id: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    institution_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Score and change
    final_score: Mapped[float] = mapped_column(Float, nullable=False)
    position_change: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Ranking criteria used
    sort_by: Mapped[str] = mapped_column(String(64), nullable=False, default="quality")
    ranking_type: Mapped[str] = mapped_column(
        String(32), nullable=False, default="institutions"
    )  # institutions, programs, etc
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Indices for historical queries
    __table_args__ = (
        Index("idx_ranking_snap_institution", "institution_id"),
        Index("idx_ranking_snap_date", "created_at"),
        Index("idx_ranking_snap_type", "ranking_type"),
    )
