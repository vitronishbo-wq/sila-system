"""create patrimonio_cultural foundation table

Revision ID: 20260306_049_patrimonio_cultural_foundation
Revises: 20260305_048_meteorologia_foundation
Create Date: 2026-03-06 10:20:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "20260306_049_patrimonio_cultural_foundation"
down_revision = "20260305_048_meteorologia_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patrimonio_cultural_assets",
        sa.Column("asset_id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("asset_type", sa.String(length=60), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("altitude", sa.Float(), nullable=True),
        sa.Column("province", sa.String(length=100), nullable=True),
        sa.Column("municipality", sa.String(length=100), nullable=True),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="registered"),
        sa.Column("classification_level", sa.String(length=40), nullable=True),
        sa.Column("classification_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("historical_period", sa.String(length=120), nullable=True),
        sa.Column("cultural_significance", sa.Text(), nullable=True),
        sa.Column("legal_reference", sa.String(length=200), nullable=True),
        sa.Column(
            "classifications", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")
        ),
        sa.Column("events", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column(
            "preservation_actions",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "latitude IS NULL OR (latitude >= -90 AND latitude <= 90)",
            name="ck_patrimonio_assets_latitude",
        ),
        sa.CheckConstraint(
            "longitude IS NULL OR (longitude >= -180 AND longitude <= 180)",
            name="ck_patrimonio_assets_longitude",
        ),
        sa.UniqueConstraint(
            "name",
            "province",
            name="uq_patrimonio_asset_name_province",
        ),
    )

    op.create_index(
        "ix_patrimonio_assets_name",
        "patrimonio_cultural_assets",
        ["name"],
        unique=False,
    )
    op.create_index(
        "ix_patrimonio_assets_asset_type",
        "patrimonio_cultural_assets",
        ["asset_type"],
        unique=False,
    )
    op.create_index(
        "ix_patrimonio_assets_province",
        "patrimonio_cultural_assets",
        ["province"],
        unique=False,
    )
    op.create_index(
        "ix_patrimonio_assets_municipality",
        "patrimonio_cultural_assets",
        ["municipality"],
        unique=False,
    )
    op.create_index(
        "ix_patrimonio_assets_status",
        "patrimonio_cultural_assets",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_patrimonio_assets_classification_level",
        "patrimonio_cultural_assets",
        ["classification_level"],
        unique=False,
    )
    op.create_index(
        "ix_patrimonio_assets_status_classification",
        "patrimonio_cultural_assets",
        ["status", "classification_level"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_patrimonio_assets_status_classification",
        table_name="patrimonio_cultural_assets",
    )
    op.drop_index(
        "ix_patrimonio_assets_classification_level", table_name="patrimonio_cultural_assets"
    )
    op.drop_index("ix_patrimonio_assets_status", table_name="patrimonio_cultural_assets")
    op.drop_index("ix_patrimonio_assets_municipality", table_name="patrimonio_cultural_assets")
    op.drop_index("ix_patrimonio_assets_province", table_name="patrimonio_cultural_assets")
    op.drop_index("ix_patrimonio_assets_asset_type", table_name="patrimonio_cultural_assets")
    op.drop_index("ix_patrimonio_assets_name", table_name="patrimonio_cultural_assets")
    op.drop_table("patrimonio_cultural_assets")
