"""Add audit columns to educacao_institution_capacities

Revision ID: 20260610_0002_add_institution_capacity_audit_columns
Revises: 20260610_0001_create_educacao_institution_capacities
Create Date: 2026-06-10 12:10:00.000000
"""
from __future__ import annotations

from alembic import op

revision: str = "20260610_0002_add_institution_capacity_audit_columns"
down_revision: str = "20260610_0001_create_educacao_institution_capacities"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE educacao_institution_capacities ADD COLUMN IF NOT EXISTS created_by VARCHAR(50)"
    )
    op.execute(
        "ALTER TABLE educacao_institution_capacities ADD COLUMN IF NOT EXISTS updated_by VARCHAR(50)"
    )
    op.execute(
        "ALTER TABLE educacao_institution_capacities ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE educacao_institution_capacities DROP COLUMN IF EXISTS is_active"
    )
    op.execute(
        "ALTER TABLE educacao_institution_capacities DROP COLUMN IF EXISTS updated_by"
    )
    op.execute(
        "ALTER TABLE educacao_institution_capacities DROP COLUMN IF EXISTS created_by"
    )
