"""Create provider_homologation_evidence table

Revision ID: 20260607_0003_create_provider_homologation_evidence
Revises: 20260607_0002_add_testing_enums_and_columns
Create Date: 2026-06-07 06:55:00.000000
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260607_0003_create_provider_homologation_evidence"
down_revision: str = "20260607_0002_add_testing_enums_and_columns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "provider_homologation_evidence",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(100), nullable=False, index=True),
        sa.Column("endpoint", sa.String(500), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("auth_ok", sa.Boolean(), default=False),
        sa.Column("payload_hash", sa.String(128), nullable=True),
        sa.Column("operator", sa.String(200), nullable=True),
        sa.Column("result", sa.String(50), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.String(50), nullable=True),
        sa.Column("updated_by", sa.String(50), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
    )
    op.create_index(
        "ix_homologation_evidence_timestamp",
        "provider_homologation_evidence",
        ["timestamp"],
    )


def downgrade() -> None:
    op.drop_index("ix_homologation_evidence_timestamp", table_name="provider_homologation_evidence")
    op.drop_table("provider_homologation_evidence")
