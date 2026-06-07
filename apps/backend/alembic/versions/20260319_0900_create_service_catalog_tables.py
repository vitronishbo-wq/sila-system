"""create service catalog tables

Revision ID: 20260319_0900_create_service_catalog_tables
Revises: 20260318_1715_add_economy_audit_columns
Create Date: 2026-03-19 09:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260319_0900_create_service_catalog_tables"
down_revision = "20260318_1715_add_economy_audit_columns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "service_catalog",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("service_code", sa.String(80), nullable=False, unique=True, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(120), nullable=True, index=True),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("price", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "service_forms",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "service_code",
            sa.String(80),
            sa.ForeignKey("service_catalog.service_code", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("version", sa.String(32), nullable=False, server_default="1"),
        sa.Column("schema", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ux_service_forms_service_code", "service_forms", ["service_code"], unique=True)


def downgrade() -> None:
    op.drop_index("ux_service_forms_service_code", table_name="service_forms")
    op.drop_table("service_forms")
    op.drop_table("service_catalog")
