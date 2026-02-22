"""Create governance module tables

Revision ID: 20250105_governance
Revises: 20250105_health
Create Date: 2025-01-05 12:00:00.000000+00:00
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20250105_governance"
down_revision = "20250105_health"
branch_labels = None
depends_on = None


def upgrade(engine_name: str = "") -> None:
    """Upgrade database schema and/or data, creating a new revision.

    Args:
        engine_name: Database engine name. If not provided, applies to all engines.
    """
    if engine_name and engine_name != "postgresql":
        return

    with op.get_context().begin_transaction():
        # ========================================================================
        # Institutions Table
        # ========================================================================
        op.create_table(
            "institutions",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("name", sa.String(length=200), nullable=False),
            sa.Column("acronym", sa.String(length=50), nullable=True),
            sa.Column("institution_type", sa.String(length=100), nullable=True),
            sa.Column("jurisdiction", sa.String(length=200), nullable=True),
            sa.Column("description", sa.String(length=2000), nullable=True),
            sa.Column("founding_date", sa.DateTime(timezone=True), nullable=True),
            sa.Column("website", sa.String(length=200), nullable=True),
            sa.Column(
                "contact_info", postgresql.JSON(astext_type=sa.Text()), nullable=True
            ),
            sa.Column(
                "leadership", postgresql.JSON(astext_type=sa.Text()), nullable=True
            ),
            sa.Column(
                "parent_institution_id", postgresql.UUID(as_uuid=True), nullable=True
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(
                ["parent_institution_id"], ["institutions.id"], ondelete="SET NULL"
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_institutions_id"), "institutions", ["id"], unique=False
        )
        op.create_index(
            op.f("ix_institutions_name"), "institutions", ["name"], unique=False
        )
        op.create_index(
            op.f("ix_institutions_institution_type"),
            "institutions",
            ["institution_type"],
            unique=False,
        )
        op.create_index(
            op.f("ix_institutions_parent_institution_id"),
            "institutions",
            ["parent_institution_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_institutions_deleted_at"),
            "institutions",
            ["deleted_at"],
            unique=False,
        )

        # ========================================================================
        # Mandates Table
        # ========================================================================
        op.create_table(
            "mandates",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("title", sa.String(length=200), nullable=False),
            sa.Column("description", sa.String(length=2000), nullable=True),
            sa.Column("mandate_type", sa.String(length=100), nullable=True),
            sa.Column("issuing_authority", sa.String(length=200), nullable=True),
            sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
            sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "status", sa.String(length=50), nullable=False, server_default="active"
            ),
            sa.Column("scope", postgresql.JSON(astext_type=sa.Text()), nullable=True),
            sa.Column(
                "related_documents",
                postgresql.JSON(astext_type=sa.Text()),
                nullable=True,
            ),
            sa.Column("institution_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(
                ["institution_id"], ["institutions.id"], ondelete="SET NULL"
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_mandates_id"), "mandates", ["id"], unique=False)
        op.create_index(op.f("ix_mandates_title"), "mandates", ["title"], unique=False)
        op.create_index(
            op.f("ix_mandates_mandate_type"), "mandates", ["mandate_type"], unique=False
        )
        op.create_index(
            op.f("ix_mandates_start_date"), "mandates", ["start_date"], unique=False
        )
        op.create_index(
            op.f("ix_mandates_status"), "mandates", ["status"], unique=False
        )
        op.create_index(
            op.f("ix_mandates_institution_id"),
            "mandates",
            ["institution_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_mandates_deleted_at"), "mandates", ["deleted_at"], unique=False
        )

        # ========================================================================
        # Council Meetings Table
        # ========================================================================
        op.create_table(
            "council_meetings",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("title", sa.String(length=200), nullable=False),
            sa.Column("description", sa.String(length=1000), nullable=True),
            sa.Column("location", sa.String(length=200), nullable=True),
            sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
            sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "status",
                sa.String(length=50),
                nullable=False,
                server_default="scheduled",
            ),
            sa.Column("agenda", postgresql.JSON(astext_type=sa.Text()), nullable=True),
            sa.Column("minutes", postgresql.JSON(astext_type=sa.Text()), nullable=True),
            sa.Column(
                "decisions", postgresql.JSON(astext_type=sa.Text()), nullable=True
            ),
            sa.Column(
                "participants", postgresql.JSON(astext_type=sa.Text()), nullable=True
            ),
            sa.Column("council_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_council_meetings_id"), "council_meetings", ["id"], unique=False
        )
        op.create_index(
            op.f("ix_council_meetings_title"),
            "council_meetings",
            ["title"],
            unique=False,
        )
        op.create_index(
            op.f("ix_council_meetings_start_time"),
            "council_meetings",
            ["start_time"],
            unique=False,
        )
        op.create_index(
            op.f("ix_council_meetings_status"),
            "council_meetings",
            ["status"],
            unique=False,
        )
        op.create_index(
            op.f("ix_council_meetings_council_id"),
            "council_meetings",
            ["council_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_council_meetings_deleted_at"),
            "council_meetings",
            ["deleted_at"],
            unique=False,
        )

        # ========================================================================
        # Decisions Table
        # ========================================================================
        op.create_table(
            "decisions",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("title", sa.String(length=200), nullable=False),
            sa.Column("description", sa.String(length=1000), nullable=True),
            sa.Column("decision_type", sa.String(length=100), nullable=True),
            sa.Column(
                "status",
                sa.String(length=50),
                nullable=False,
                server_default="proposed",
            ),
            sa.Column(
                "voting_record", postgresql.JSON(astext_type=sa.Text()), nullable=True
            ),
            sa.Column("effective_date", sa.DateTime(timezone=True), nullable=True),
            sa.Column("expiration_date", sa.DateTime(timezone=True), nullable=True),
            sa.Column(
                "related_documents",
                postgresql.JSON(astext_type=sa.Text()),
                nullable=True,
            ),
            sa.Column("meeting_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(
                ["meeting_id"], ["council_meetings.id"], ondelete="SET NULL"
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_decisions_id"), "decisions", ["id"], unique=False)
        op.create_index(
            op.f("ix_decisions_title"), "decisions", ["title"], unique=False
        )
        op.create_index(
            op.f("ix_decisions_decision_type"),
            "decisions",
            ["decision_type"],
            unique=False,
        )
        op.create_index(
            op.f("ix_decisions_status"), "decisions", ["status"], unique=False
        )
        op.create_index(
            op.f("ix_decisions_meeting_id"), "decisions", ["meeting_id"], unique=False
        )
        op.create_index(
            op.f("ix_decisions_deleted_at"), "decisions", ["deleted_at"], unique=False
        )


def downgrade(engine_name: str = "") -> None:
    """Downgrade database schema and/or data back to the previous revision.

    Args:
        engine_name: Database engine name. If not provided, applies to all engines.
    """
    if engine_name and engine_name != "postgresql":
        return

    with op.get_context().begin_transaction():
        # Drop tables in reverse order (respecting foreign key constraints)
        op.drop_table("decisions")
        op.drop_table("council_meetings")
        op.drop_table("mandates")
        op.drop_table("institutions")
