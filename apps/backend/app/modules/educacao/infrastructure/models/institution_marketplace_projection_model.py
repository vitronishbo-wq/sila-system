"""CQRS Read Model for Marketplace Institution Projections

This is a denormalized, optimized read model specifically designed for
marketplace discovery and search operations. It's separate from transactional
academic data to follow CQRS principles.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func as sql_func

from apps.backend.app.core.db import Base


class InstitutionMarketplaceProjectionModel(Base):
    """
    Marketplace-optimized read model for institutions.
    
    Denormalized data optimized for search, filtering, and ranking.
    Updated asynchronously via events from the institution domain.
    """

    __tablename__ = "marketplace_institution_projections"

    # Core Identity
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True, unique=True
    )

    # Basic Information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(
        String(32), nullable=False, index=True
    )  # publica, privada, comunitaria
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Location Hierarchy (indexed for filtering)
    province: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    municipality: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    district: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    neighborhood: Mapped[str] = mapped_column(String(128), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)

    # Contact Information
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Marketplace-Specific Metrics
    rating: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)
    review_count: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)

    available_slots: Mapped[Integer] = mapped_column(
        Integer, nullable=False, default=0, index=True
    )
    total_capacity: Mapped[Integer] = mapped_column(Integer, nullable=False, default=0)
    occupancy_rate: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)

    # Financial Information
    monthly_fee_min: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)
    monthly_fee_max: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)
    monthly_fee_avg: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)

    # Performance Indicators
    approval_rate: Mapped[Float] = mapped_column(
        Float, nullable=False, default=0.0
    )  # % of applications approved
    transfer_acceptance_rate: Mapped[Float] = mapped_column(
        Float, nullable=False, default=0.0
    )  # % of transfers accepted
    retention_rate: Mapped[Float] = mapped_column(
        Float, nullable=False, default=0.0
    )  # % of students retained

    # Academic Performance
    average_academic_performance: Mapped[Float] = mapped_column(
        Float, nullable=False, default=0.0
    )
    student_satisfaction: Mapped[Float] = mapped_column(
        Float, nullable=False, default=0.0
    )

    # Specializations (JSON for flexible representation)
    specializations: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list
    )
    teaching_modalities: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list
    )  # presencial, remoto, hibrido
    educational_levels: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list
    )  # primario, secundario, superior

    # Special Needs Support
    supports_special_needs: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    special_needs_types: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list
    )

    # Quality Indicators
    accreditation_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending"
    )  # pending, accredited, conditionally_accredited
    quality_index: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)

    # Distance Score (calculated from student location)
    # This should be updated based on student profile
    default_distance_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )

    # Marketplace Visibility
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    featured_until: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Full-text search vector (for PostgreSQL FTS)
    search_vector: Mapped[Optional[str]] = mapped_column(
        TSVECTOR, nullable=True, index=True
    )

    # Metadata
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, nullable=False, default=dict)

    # Audit Trail
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    last_indexed_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Indexes for common query patterns
    __table_args__ = (
        Index(
            "idx_marketplace_location",
            "province",
            "municipality",
            "district",
            postgresql_using="btree",
        ),
        Index(
            "idx_marketplace_financial",
            "monthly_fee_min",
            "monthly_fee_max",
            postgresql_using="btree",
        ),
        Index(
            "idx_marketplace_performance",
            "rating",
            "approval_rate",
            "quality_index",
            postgresql_using="btree",
        ),
        Index("idx_marketplace_active", "is_active", "is_featured"),
        Index("idx_marketplace_capacity", "available_slots", "occupancy_rate"),
        Index(
            "idx_marketplace_fts",
            "search_vector",
            postgresql_using="gin",
        ),
    )
