"""Create educacao_institution_capacities table

Revision ID: 20260610_0001_create_educacao_institution_capacities
Revises: 20260607_0003_create_provider_homologation_evidence
Create Date: 2026-06-10 12:00:00.000000
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260610_0001_create_educacao_institution_capacities"
down_revision: str = "20260607_0003_create_provider_homologation_evidence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS educacao_institution_capacities (
            id UUID PRIMARY KEY,
            institution_id UUID NOT NULL,
            grade VARCHAR(32) NOT NULL,
            shift VARCHAR(32) NOT NULL,
            capacity_total INTEGER NOT NULL,
            capacity_used INTEGER NOT NULL DEFAULT 0,
            capacity_reserved INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ
        )
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'uq_institution_capacity'
            ) THEN
                ALTER TABLE educacao_institution_capacities
                ADD CONSTRAINT uq_institution_capacity UNIQUE (institution_id, grade, shift);
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'chk_capacity_total_positive'
            ) THEN
                ALTER TABLE educacao_institution_capacities
                ADD CONSTRAINT chk_capacity_total_positive CHECK (capacity_total > 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'chk_capacity_used_non_negative'
            ) THEN
                ALTER TABLE educacao_institution_capacities
                ADD CONSTRAINT chk_capacity_used_non_negative CHECK (capacity_used >= 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'chk_capacity_reserved_non_negative'
            ) THEN
                ALTER TABLE educacao_institution_capacities
                ADD CONSTRAINT chk_capacity_reserved_non_negative CHECK (capacity_reserved >= 0);
            END IF;
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'chk_capacity_total_not_exceeded'
            ) THEN
                ALTER TABLE educacao_institution_capacities
                ADD CONSTRAINT chk_capacity_total_not_exceeded CHECK (capacity_used + capacity_reserved <= capacity_total);
            END IF;
        END $$;
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_institution_capacities_institution_id ON educacao_institution_capacities (institution_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_institution_capacities_grade ON educacao_institution_capacities (grade)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_educacao_institution_capacities_shift ON educacao_institution_capacities (shift)"
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS educacao_institution_capacities CASCADE")
