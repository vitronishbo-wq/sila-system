"""FASE 3.2.1 - Institution Marketplace Projection CQRS Read Model

Revision ID: 20260527_001_marketplace_institution_projection
Revises: 20260524_001_foundation_outbox
Create Date: 2026-05-27 00:00:00.000000

This migration creates the CQRS read model for the educational marketplace,
separating read optimization from transactional academic data.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID

revision = "20260527_001_marketplace_institution_projection"
down_revision = "20260524_001_foundation_outbox"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "marketplace_institution_projections",
        sa.Column("id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("institution_id", UUID(as_uuid=True), nullable=False, unique=True),
        # Basic Information
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        # Location Hierarchy
        sa.Column("province", sa.String(128), nullable=False),
        sa.Column("municipality", sa.String(128), nullable=False),
        sa.Column("district", sa.String(128), nullable=False),
        sa.Column("neighborhood", sa.String(128), nullable=True),
        sa.Column("address", sa.Text, nullable=True),
        # Contact
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(64), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        # Marketplace Metrics
        sa.Column("rating", sa.Float, nullable=False, default=0.0),
        sa.Column("review_count", sa.Integer, nullable=False, default=0),
        sa.Column("available_slots", sa.Integer, nullable=False, default=0),
        sa.Column("total_capacity", sa.Integer, nullable=False, default=0),
        sa.Column("occupancy_rate", sa.Float, nullable=False, default=0.0),
        # Financial
        sa.Column("monthly_fee_min", sa.Float, nullable=False, default=0.0),
        sa.Column("monthly_fee_max", sa.Float, nullable=False, default=0.0),
        sa.Column("monthly_fee_avg", sa.Float, nullable=False, default=0.0),
        # Performance
        sa.Column("approval_rate", sa.Float, nullable=False, default=0.0),
        sa.Column("transfer_acceptance_rate", sa.Float, nullable=False, default=0.0),
        sa.Column("retention_rate", sa.Float, nullable=False, default=0.0),
        # Academic
        sa.Column("average_academic_performance", sa.Float, nullable=False, default=0.0),
        sa.Column("student_satisfaction", sa.Float, nullable=False, default=0.0),
        # Flexible Data
        sa.Column("specializations", JSONB, nullable=False, default=list),
        sa.Column("teaching_modalities", JSONB, nullable=False, default=list),
        sa.Column("educational_levels", JSONB, nullable=False, default=list),
        # Special Needs
        sa.Column("supports_special_needs", sa.Boolean, nullable=False, default=False),
        sa.Column("special_needs_types", JSONB, nullable=False, default=list),
        # Quality
        sa.Column("accreditation_status", sa.String(32), nullable=False, default="pending"),
        sa.Column("quality_index", sa.Float, nullable=False, default=0.0),
        sa.Column("default_distance_score", sa.Float, nullable=False, default=0.0),
        # Marketplace Control
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
        sa.Column("is_featured", sa.Boolean, nullable=False, default=False),
        sa.Column("featured_until", sa.DateTime(timezone=True), nullable=True),
        # Full-text search vector
        sa.Column("search_vector", TSVECTOR, nullable=True),
        # Metadata
        sa.Column("metadata", JSONB, nullable=False, default=dict),
        # Audit
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_indexed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Create indexes for common query patterns
    op.create_index(
        "idx_marketplace_institution_id",
        "marketplace_institution_projections",
        ["institution_id"],
    )
    op.create_index(
        "idx_marketplace_location",
        "marketplace_institution_projections",
        ["province", "municipality", "district"],
    )
    op.create_index(
        "idx_marketplace_financial",
        "marketplace_institution_projections",
        ["monthly_fee_min", "monthly_fee_max"],
    )
    op.create_index(
        "idx_marketplace_performance",
        "marketplace_institution_projections",
        ["rating", "approval_rate", "quality_index"],
    )
    op.create_index(
        "idx_marketplace_active",
        "marketplace_institution_projections",
        ["is_active", "is_featured"],
    )
    op.create_index(
        "idx_marketplace_capacity",
        "marketplace_institution_projections",
        ["available_slots", "occupancy_rate"],
    )
    op.create_index(
        "idx_marketplace_fts",
        "marketplace_institution_projections",
        ["search_vector"],
        postgresql_using="gin",
    )


def downgrade():
    op.drop_table("marketplace_institution_projections")
