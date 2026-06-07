"""Add testing enum values and measurement_mode column

Revision ID: 20260607_0002_add_testing_enums_and_columns
Revises: 20260607_0001_create_provider_operations_tables
Create Date: 2026-06-07 05:20:00.000000
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260607_0002_add_testing_enums_and_columns"
down_revision: str = "20260607_0001_create_provider_operations_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add "testing" to contract_status enum
    op.execute("ALTER TYPE contract_status ADD VALUE IF NOT EXISTS 'testing'")
    # Add "testing" and "mock_live" to cert_status enum
    op.execute("ALTER TYPE cert_status ADD VALUE IF NOT EXISTS 'testing'")
    op.execute("ALTER TYPE cert_status ADD VALUE IF NOT EXISTS 'mock_live'")
    # Add measurement_mode column to sla_snapshots
    op.add_column("provider_sla_snapshots",
        sa.Column("measurement_mode", sa.String(length=50),
                  nullable=False, server_default="simulated"),
    )


def downgrade() -> None:
    op.drop_column("provider_sla_snapshots", "measurement_mode")
