"""create service requests tables

Revision ID: 001_create_service_requests
Revises:
Create Date: 2024-01-01
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID

revision = "001_create_service_requests"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "service_requests",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("request_number", sa.String(50), nullable=True, unique=True),
        sa.Column("citizen_id", UUID(as_uuid=True), nullable=False),
        sa.Column("created_by_user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("assigned_to_user_id", UUID(as_uuid=True), nullable=True),
        sa.Column("service_type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="RASCUNHO"),
        sa.Column("priority", sa.String(20), nullable=False, server_default="MEDIA"),
        sa.Column("channel", sa.String(20), nullable=False, server_default="WEB"),
        sa.Column("workflow_instance_id", UUID(as_uuid=True), nullable=True),
        sa.Column("workflow_data", JSONB(), nullable=True),
        sa.Column("metadata", JSONB(), nullable=True),
        sa.Column("tags", ARRAY(sa.String), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.text("now()")),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sla_due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sla_breached", sa.Boolean, nullable=False, server_default="false"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_service_requests_request_number", "service_requests", ["request_number"])
    op.create_index("ix_service_requests_citizen_id", "service_requests", ["citizen_id"])
    op.create_index(
        "ix_service_requests_assigned_to_user_id", "service_requests", ["assigned_to_user_id"]
    )
    op.create_index("ix_service_requests_service_type", "service_requests", ["service_type"])
    op.create_index("ix_service_requests_status", "service_requests", ["status"])
    op.create_index(
        "ix_service_requests_workflow_instance_id", "service_requests", ["workflow_instance_id"]
    )
    op.create_index(
        "ix_service_requests_citizen_status", "service_requests", ["citizen_id", "status"]
    )
    op.create_index(
        "ix_service_requests_assignee_status", "service_requests", ["assigned_to_user_id", "status"]
    )
    op.create_index("ix_service_requests_created_at", "service_requests", ["created_at"])
    op.create_index("ix_service_requests_submitted_at", "service_requests", ["submitted_at"])
    op.create_index("ix_service_requests_deadline", "service_requests", ["deadline"])
    op.create_index("ix_service_requests_sla_due", "service_requests", ["sla_due_at"])


def downgrade():
    op.drop_table("service_requests")
