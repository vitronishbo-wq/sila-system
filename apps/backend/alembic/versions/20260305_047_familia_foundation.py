"""create familia foundation tables

Revision ID: 20260305_047_familia_foundation
Revises: 20260305_046_cultura_slice3_espacos_projetos_editais
Create Date: 2026-03-05 10:30:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260305_047_familia_foundation"
down_revision = "20260305_046_cultura_slice3_espacos_projetos_editais"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS family_aggregates (
            id UUID PRIMARY KEY,
            code VARCHAR(50) NOT NULL UNIQUE,
            head_citizen_id UUID NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
            metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            deleted_at TIMESTAMPTZ NULL
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_family_head_active
        ON family_aggregates (head_citizen_id, status)
        WHERE status = 'ACTIVE'
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS family_members (
            id UUID PRIMARY KEY,
            family_id UUID NOT NULL REFERENCES family_aggregates(id) ON DELETE CASCADE,
            citizen_id UUID NOT NULL,
            role VARCHAR(20) NOT NULL,
            joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            left_at TIMESTAMPTZ NULL,
            metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
            CONSTRAINT uq_family_member_unique UNIQUE (family_id, citizen_id)
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_member_citizen_active
        ON family_members (citizen_id, left_at)
        WHERE left_at IS NULL
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS family_relationships (
            id UUID PRIMARY KEY,
            citizen_a_id UUID NOT NULL,
            citizen_b_id UUID NOT NULL,
            relationship_type VARCHAR(32) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
            start_date DATE NOT NULL,
            end_date DATE NULL,
            legal_document_id VARCHAR(100) NULL,
            metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_relationship_active_pair
        ON family_relationships (citizen_a_id, citizen_b_id, status)
        WHERE status = 'ACTIVE'
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_relationship_type
        ON family_relationships (relationship_type)
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS dependency_records (
            id UUID PRIMARY KEY,
            dependent_citizen_id UUID NOT NULL,
            guardian_citizen_id UUID NOT NULL,
            dependency_type VARCHAR(20) NOT NULL,
            program_reference VARCHAR(100) NULL,
            start_date DATE NOT NULL,
            end_date DATE NULL,
            metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_dependency_active
        ON dependency_records (dependent_citizen_id, end_date)
        WHERE end_date IS NULL
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS family_domain_events (
            id UUID PRIMARY KEY,
            aggregate_id UUID NOT NULL REFERENCES family_aggregates(id) ON DELETE CASCADE,
            event_type VARCHAR(120) NOT NULL,
            event_version INTEGER NOT NULL,
            event_payload JSONB NOT NULL,
            occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            published BOOLEAN NOT NULL DEFAULT FALSE
        )
        """
    )
    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_events_aggregate_seq
        ON family_domain_events (aggregate_id, event_version)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_family_events_publish
        ON family_domain_events (published, occurred_at)
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS family_composition_view (
            family_id UUID PRIMARY KEY,
            head_citizen_id UUID NOT NULL,
            head_name VARCHAR(200) NOT NULL DEFAULT '',
            member_count INTEGER NOT NULL DEFAULT 0,
            dependents_count INTEGER NOT NULL DEFAULT 0,
            active_relationships INTEGER NOT NULL DEFAULT 0,
            composition_json JSONB NOT NULL DEFAULT '{}'::jsonb,
            last_updated TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_composition_head
        ON family_composition_view (head_citizen_id)
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS family_composition_view")
    op.execute("DROP TABLE IF EXISTS family_domain_events")
    op.execute("DROP TABLE IF EXISTS dependency_records")
    op.execute("DROP TABLE IF EXISTS family_relationships")
    op.execute("DROP TABLE IF EXISTS family_members")
    op.execute("DROP TABLE IF EXISTS family_aggregates")
