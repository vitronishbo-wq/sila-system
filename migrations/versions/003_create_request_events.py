"""Create request events table

Revision ID: 003_create_request_events
Revises: 002_create_attachments
Create Date: 2026-02-18
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "003_create_request_events"
down_revision = "002_create_attachments"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "service_request_events",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("payload", sa.JSON, nullable=True),
        sa.Column("actor_id", UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["request_id"], ["service_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_service_request_events_request", "service_request_events", ["request_id"])
    op.create_index("ix_service_request_events_created", "service_request_events", ["created_at"])
    op.create_index(
        "ix_service_request_events_request_created",
        "service_request_events",
        ["request_id", "created_at"],
    )


def downgrade():
    op.drop_table("service_request_events")
