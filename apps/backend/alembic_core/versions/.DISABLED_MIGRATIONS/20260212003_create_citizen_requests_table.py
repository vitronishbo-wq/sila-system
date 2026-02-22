"""Create citizen_requests table for workflow routing

Revision ID: 20260212003
Revises: 20260212002
Create Date: 2026-02-12 10:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "20260212003"
down_revision = "20260212002"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "citizen_requests",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("citizen_id", UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", UUID(as_uuid=True), nullable=False),
        sa.Column("territory_id", UUID(as_uuid=True), nullable=False),
        sa.Column("original_territory_id", UUID(as_uuid=True), nullable=False),
        sa.Column("state", sa.String(50), nullable=False, server_default="SUBMETIDO"),
        sa.Column("data", JSONB, nullable=True),
        sa.Column("routing_justification", sa.Text, nullable=True),
        sa.Column("assigned_to_id", UUID(as_uuid=True), nullable=True),
        sa.Column("assigned_to_role", sa.String(50), nullable=True),
        sa.Column("escalation_reason", sa.Text, nullable=True),
        sa.Column("escalated_from_id", UUID(as_uuid=True), nullable=True),
        sa.Column("escalated_at", sa.DateTime, nullable=True),
        sa.Column("resolved_at", sa.DateTime, nullable=True),
        sa.Column("resolution_notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
        
        sa.ForeignKeyConstraint(["citizen_id"], ["citizen_fuc.citizen_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["territory_id"], ["territories.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["original_territory_id"], ["territories.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["assigned_to_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["escalated_from_id"], ["citizen_requests.id"], ondelete="SET NULL"),
        
        sa.Index("ix_citizen_requests_citizen", "citizen_id"),
        sa.Index("ix_citizen_requests_territory", "territory_id"),
        sa.Index("ix_citizen_requests_state", "state"),
        sa.Index("ix_citizen_requests_assigned", "assigned_to_id"),
        sa.Index("ix_citizen_requests_created", "created_at"),
    )

def downgrade():
    op.drop_table("citizen_requests")
